<p class="blog_meta">
<?php
_e('By ', 'nimbus');
the_author_posts_link();
_e(' on ', 'nimbus');
the_time(get_option('date_format'));
?>
</p>
