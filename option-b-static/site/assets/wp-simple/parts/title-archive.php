<h1 id="blog_feed_title">
<?php
if (is_author()) {
    $curauth = (isset($_GET['author_name'])) ? get_user_by('slug', $author_name) : get_userdata(intval($author));
    echo "Posts By: " . $curauth->display_name;
} else if (is_date()) {
    echo "Viewing: ";
    if (is_day()) {
        the_time('F jS, Y');
    } else if (is_month()) {
        the_time('F, Y');
    } else if (is_year()) {
        the_time('Y');
    }
} else if (is_archive()){
    single_cat_title(__( 'Viewing: ', 'nimbus'));
}
?>
</h1>
