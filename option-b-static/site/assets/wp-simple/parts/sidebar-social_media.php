<?php
$nimbus_social_type = array("nimbus_facebook_url", "nimbus_linkedin_url", "nimbus_twitter_url", "nimbus_youtube_url", "nimbus_google_plus_url", "nimbus_mail_url");
foreach ($nimbus_social_type as $key => $id) {
    $$id = trim(nimbus_get_option($id));
    if (empty($$id)) {
        if (nimbus_get_option('nimbus_example_content') == "on") {
            $$id = '#';
        }
    } else {
        $id = $$id;
    }
}

?>
<h3 class="social_title"><?php echo nimbus_get_option('nimbus_social_sidebar_title'); ?></h3>
<ul id='social_media_icons'>
    <?php
    if (!empty($nimbus_facebook_url)) {
        echo"<li id='facebook_icon'><a target='_blank' href='" . $nimbus_facebook_url . "'></a></li>";
    }
    if (!empty($nimbus_linkedin_url)) {
        echo"<li id='linkedin_icon'><a target='_blank' href='" . $nimbus_linkedin_url . "'></a></li>";
    }
    if (!empty($nimbus_twitter_url)) {
        echo"<li id='twitter_icon'><a target='_blank' href='" . $nimbus_twitter_url . "'></a></li>";
    }
    if (!empty($nimbus_youtube_url)) {
        echo"<li id='youtube_icon'><a target='_blank' href='" . $nimbus_youtube_url . "'></a></li>";
    }
    if (!empty($nimbus_google_plus_url)) {
        echo"<li id='google_plus_icon'><a target='_blank' href='" . $nimbus_google_plus_url . "'></a></li>";
    }
    if (!empty($nimbus_mail_url)) {
        echo"<li id='mail_icon'><a href='mailto:" . nimbus_get_option('nimbus_mail_url') . "'></a></li>";
    }
    if (nimbus_get_option('nimbus_hide_rss_icon') == 0) {
        $nimbus_alt_rss_url = nimbus_get_option('nimbus_alt_rss_url');
        if (!empty($nimbus_alt_rss_url)) {
            echo"<li id='rss_icon'><a href='" . $nimbus_alt_rss_url . "'></a></li>";
        } else {
        ?>
            <li id='rss_icon'><a href='<?php echo bloginfo('rss2_url'); ?>'></a></li>
        <?php
        }
    }
    ?>
</ul>
<div class='clear20'></div>


