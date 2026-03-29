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
                                if (get_post_meta($post->ID, 'include_image_on_page', true) == "true") {
                                    get_template_part( 'parts/image', '740_420');
                                }
                            }
                            ?>
                            <h1><?php get_template_part( 'parts/title', 'page'); ?></h1>
                            <?php
                            the_content();
                            n_clear();
                            get_template_part( 'parts/wp_link_pages');
                            comments_template();
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

