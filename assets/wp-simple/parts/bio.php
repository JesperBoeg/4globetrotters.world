<?php
if (is_author()) {
    $nimbus_curauth = (isset($_GET['author_name'])) ? get_user_by('slug', $author_name) : get_userdata(intval($author));
}
?>
<div class="row bio_wrap">
    <div class="col-md-2">
        <?php
        if (is_author()) {
            echo get_avatar($nimbus_curauth->user_email, '171');
        } else {
            echo get_avatar(get_the_author_meta('email'), '105');
        }
        ?>
    </div>
    <div class="col-md-10">
        <?php
        if (is_author()) {
        ?>
            <h3><?php echo $nimbus_curauth->display_name; ?></h3>
            <p><?php echo $nimbus_curauth->user_description; ?></p>
        <?php
        } else {
        ?>
            <h3><?php the_author_posts_link(); ?></h3>
            <p><?php the_author_meta('description'); ?></p>
        <?php
        }
        ?>

    </div>
</div>

