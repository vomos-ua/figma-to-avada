<?php
/**
 * Plugin Name: LP Meta Research
 * Description: TEMPORARY plugin. Registers REST endpoint /wp-json/lp-research/v1/meta/{id} for inspecting Avada _fusion meta. Auth-gated to admins. Delete plugin after research is done.
 * Version: 0.1.0
 * Author: Linked Promo
 * Requires PHP: 7.4
 * Requires at least: 6.9
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('rest_api_init', function () {
    register_rest_route('lp-research/v1', '/meta/(?P<id>\d+)', [
        'methods'  => 'GET',
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
        'args' => [
            'id' => [
                'validate_callback' => function ($value) {
                    return is_numeric($value) && (int) $value > 0;
                },
                'sanitize_callback' => 'absint',
            ],
        ],
        'callback' => function ($req) {
            $id = (int) $req['id'];
            $post = get_post($id);
            if (!$post) {
                return new WP_Error('not_found', "Post {$id} not found", ['status' => 404]);
            }
            $raw = get_post_meta($id);
            $unwrapped = [];
            foreach ($raw as $key => $values) {
                if (is_array($values) && count($values) === 1) {
                    $unwrapped[$key] = maybe_unserialize($values[0]);
                } else {
                    $unwrapped[$key] = array_map('maybe_unserialize', $values);
                }
            }
            return [
                'post_id'    => $id,
                'post_type'  => $post->post_type,
                'post_title' => $post->post_title,
                'meta'       => $unwrapped,
            ];
        },
    ]);
});
