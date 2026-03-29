<div id="post-<?php the_ID(); ?>" <?php post_class('blog_small_wrap'); ?>>
    <?php
    get_template_part( 'parts/image', '105_90');
    ?>
    <h4><a href="<?php the_permalink(); ?>"><?php get_template_part( 'parts/title', 'post'); ?></a></h4>
    <?php
    get_template_part( 'parts/blog', 'meta_line');
    ?>
    <p class="excerpt">
    <?php
    echo get_the_excerpt()
    ?>
    </p>
    <div class="clear"></div>
</div>