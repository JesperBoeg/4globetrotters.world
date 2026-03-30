<!doctype html>
<html <?php language_attributes(); ?>>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title><?php wp_title(); ?></title>
        <link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />
        <?php
        wp_head();
        ?>
    </head>
    <body <?php body_class(); ?>>
        <header>
            <?php
            get_template_part( 'parts/banner');
            get_template_part( 'parts/menu');
            ?>
        </header>