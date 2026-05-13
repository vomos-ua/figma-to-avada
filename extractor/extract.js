// Minimal Bridge-based extractor for figma-console MCP
// Sent as payload to figma_execute. Returns a structured brief JSON.
//
// Usage from Claude Code:
//   1. Substitute __NODE_ID__ (e.g. '62:2')
//   2. Call mcp__figma-console__figma_execute with this code
//   3. Save returned JSON to output/{site}/{page}/brief/sections/{n}-{name}.json
//
// Key behavior: decorative frames (chevron patterns, glows, textures) are NOT
// walked — they get marked as `decorative: true` so the generator knows to
// emit them as background-image instead of element tree.

const NODE_ID = '__NODE_ID__';

const DECORATIVE_NAME_RE = /chevron|glow|pattern|texture|noise|particles|grid bg|decoration/i;

function rgb(c) {
  if (!c) return null;
  return '#' + [c.r, c.g, c.b]
    .map((v) => Math.round(v * 255).toString(16).padStart(2, '0'))
    .join('').toUpperCase();
}

function isDecorative(node) {
  if (DECORATIVE_NAME_RE.test(node.name || '')) return true;
  // Single-color ellipse with gradient_radial fill = glow effect
  if (node.type === 'ELLIPSE' && node.fills?.length === 1 && node.fills[0].type === 'GRADIENT_RADIAL') {
    return true;
  }
  return false;
}

function extractFills(node) {
  if (!node.fills || node.fills === figma.mixed) return [];
  return node.fills.filter((f) => f.visible !== false).map((f) => {
    const base = { type: f.type, opacity: f.opacity ?? 1 };
    if (f.type === 'SOLID') return { ...base, color: rgb(f.color) };
    if (f.type === 'GRADIENT_LINEAR' || f.type === 'GRADIENT_RADIAL' || f.type === 'GRADIENT_ANGULAR') {
      return {
        ...base,
        stops: (f.gradientStops || []).map((s) => ({
          position: s.position, color: rgb(s.color), alpha: s.color.a ?? 1,
        })),
      };
    }
    if (f.type === 'IMAGE') return { ...base, imageHash: f.imageHash, scaleMode: f.scaleMode };
    return base;
  });
}

function extractStrokes(node) {
  if (!node.strokes || !node.strokes.length) return null;
  return {
    weight: node.strokeWeight,
    align: node.strokeAlign,
    colors: node.strokes.map((s) => (s.type === 'SOLID' ? rgb(s.color) : null)).filter(Boolean),
  };
}

function extractText(node) {
  return {
    characters: node.characters,
    fontFamily: node.fontName?.family,
    fontStyle: node.fontName?.style,
    fontSize: node.fontSize,
    lineHeight: node.lineHeight,
    letterSpacing: node.letterSpacing,
    textAlignH: node.textAlignHorizontal,
    textAlignV: node.textAlignVertical,
    textCase: node.textCase,
    textDecoration: node.textDecoration,
  };
}

function extractLayout(node) {
  if (node.layoutMode === undefined) return null;
  if (node.layoutMode === 'NONE') return { mode: 'NONE' };
  return {
    mode: node.layoutMode,
    primaryAxisSizing: node.primaryAxisSizingMode,
    counterAxisSizing: node.counterAxisSizingMode,
    primaryAxisAlign: node.primaryAxisAlignItems,
    counterAxisAlign: node.counterAxisAlignItems,
    itemSpacing: node.itemSpacing,
    paddingTop: node.paddingTop,
    paddingRight: node.paddingRight,
    paddingBottom: node.paddingBottom,
    paddingLeft: node.paddingLeft,
  };
}

function extractEffects(node) {
  if (!node.effects || !node.effects.length) return null;
  return node.effects.filter((e) => e.visible !== false).map((e) => ({
    type: e.type,
    color: e.color ? rgb(e.color) : null,
    alpha: e.color?.a ?? null,
    offset: e.offset,
    radius: e.radius,
    spread: e.spread,
  }));
}

function walk(node, depth = 0, maxDepth = 20) {
  if (depth > maxDepth) return { type: 'TRUNCATED', name: node.name };

  const base = {
    id: node.id,
    name: node.name,
    type: node.type,
    visible: node.visible !== false,
    bounds: {
      x: Math.round(node.x ?? 0),
      y: Math.round(node.y ?? 0),
      w: Math.round(node.width ?? 0),
      h: Math.round(node.height ?? 0),
    },
    opacity: node.opacity ?? 1,
    cornerRadius: node.cornerRadius,
    fills: extractFills(node),
  };

  const strokes = extractStrokes(node);
  if (strokes) base.strokes = strokes;

  const effects = extractEffects(node);
  if (effects) base.effects = effects;

  // Decorative: stop walking. Generator will export this node as background image.
  if (isDecorative(node)) {
    base.decorative = true;
    base.exportHint = 'background-image';
    return base;
  }

  if (node.type === 'TEXT') {
    base.text = extractText(node);
  }

  if (node.type === 'INSTANCE') {
    base.componentId = node.mainComponent?.id;
    base.componentName = node.mainComponent?.name;
  }

  const layout = extractLayout(node);
  if (layout) base.layout = layout;

  if (node.children && node.children.length) {
    base.children = node.children.map((c) => walk(c, depth + 1, maxDepth));
  }

  return base;
}

const targetId = NODE_ID;
const target = targetId === '__NODE_ID__' ? figma.currentPage : await figma.getNodeByIdAsync(targetId);

if (!target) {
  return { error: 'Node not found', id: targetId };
}

const brief = {
  meta: {
    extractedAt: new Date().toISOString(),
    figmaFile: figma.root.name,
    pageName: figma.currentPage.name,
    rootNodeId: target.id,
    rootNodeName: target.name,
    extractorVersion: '0.1.0-decorative-skip',
  },
  tree: walk(target),
};

return brief;
