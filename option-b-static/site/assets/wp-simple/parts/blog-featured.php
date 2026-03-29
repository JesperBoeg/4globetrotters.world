<div id="post-<?php the_ID(); ?>" <?php post_class('blog_featured_wrap'); ?>>
    <?php
    get_template_part( 'parts/image', '740_420');
    n_clear();
    ?>
    <h2 class="blog_feature_title"><a href="<?php the_permalink(); ?>"><?php get_template_part( 'parts/title', 'post'); ?></a></h2>
    <?php
    get_template_part( 'parts/blog', 'meta_line');
    the_content(__('Read more...', 'nimbus'));
    get_template_part( 'parts/blog', 'tax');
    ?>
</div>