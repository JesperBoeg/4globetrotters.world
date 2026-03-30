<?php
$nimbus_post_meta_single = nimbus_get_option('nimbus_post_meta_single');
?>

<div id="page_content_row">
    <div class="container">
        <div class="row">
            <div class="col-md-8 editable">
                <div>
                    <?php
                    if (have_posts()) {
                        while (have_posts()) {
                            the_post();
                            $paged = $wp_query->get( 'page' );
                            if ( ! $paged || $paged < 2 )  {
                                if (get_post_format() == false) {
                                    if (!is_attachment()) {
                                        if (get_post_meta($post->ID, 'include_image_on_page', true) == "true") {
                                            get_template_part( 'parts/image', '740_420');
                                        }
                                    }
                                }
                            }
                            if ($nimbus_post_meta_single['title']) {
                            ?>
                                <h1><?php get_template_part( 'parts/title', 'post'); ?></h1>
                            <?php
                            }
                            get_template_part( 'parts/blog', 'meta_line');
                            the_content();
                            n_clear();
                            get_template_part( 'parts/wp_link_pages');
                            get_template_part( 'parts/blog', 'tax');
                            if (nimbus_get_option('display_bio') == 1) {
                                get_template_part( 'parts/bio');
                            }
                            comments_template();
                            get_template_part( 'parts/blog', 'single_post_nav');
                        }
                    } else {
                            get_template_part( 'parts/error', 'no_results');
                    }
                    ?>
                </div>
            </div>
            <?php
            get_sidebar();
            ?>
        </div>
    </div>
</div>

