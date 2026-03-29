<div class="frontpage_featured_item hidden-xs">
    <a href="<?php the_permalink(); ?>">
        <?php
        get_template_part( 'parts/image', '270_170');
        ?>
    </a>
    <h4><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h4>
</div>
<div class="frontpage_featured_item visible-xs">
    <a href="<?php the_permalink(); ?>">
        <?php
        get_template_part( 'parts/image', '105_90');
        ?>
    </a>
    <h4><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h4>
    <p class="excerpt">
        <?php
        echo get_the_excerpt()
        ?>
    </p>
</div>
<div class="clear30 visible-xs"></div>