<?php
/**
 * Plugin Name: LP Meta Inspector
 * Description: TEMPORARY plugin. Registers lp/inspect-post-meta ability for reverse-engineering Avada _fusion meta structure. Auth-gated to admins. Delete plugin after research is done.
 * Version: 0.1.0
 * Author: Linked Promo
 * Requires PHP: 7.4
 * Requires at least: 6.9
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('abilities_api_init', function () {
    if (!function_exists('wp_register_ability')) {
        return;
    }

    wp_register_ability('lp/inspect-post-meta', [
        'label'       => 'Inspect Post Meta',
        'description' => 'Returns all post_meta for a given post ID, with serialized values unwrapped. Auth-gated to admins. Used for reverse-engineering plugin meta keys like Avada _fusion.',
        'category'    => 'lp-internal',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'post_id' => [
                    'type'        => 'integer',
                    'description' => 'WordPress post ID to inspect',
                ],
            ],
            'required' => ['post_id'],
        ],
        'output_schema' => [
            'type'        => 'object',
            'description' => 'Map of meta_key => unserialized meta_value (or array of values when key has multiple)',
        ],
        'execute_callback' => function ($input) {
            $id = (int) ($input['post_id'] ?? 0);
            if ($id <= 0) {
                return new WP_Error('invalid_id', 'post_id must be a positive integer');
            }

            $post = get_post($id);
            if (!$post) {
                return new WP_Error('not_found', "Post {$id} not found");
            }

            $raw = get_post_meta($id);
            return array_map(function ($v) {
                if (is_array($v) && count($v) === 1) {
                    return maybe_unserialize($v[0]);
                }
                return array_map('maybe_unserialize', $v);
            }, $raw);
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
        'meta' => [
            'mcp' => [
                'public' => true,
            ],
        ],
    ]);
});
