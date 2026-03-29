    <div id="footer_row">
        <div class="container">
            <div class="row footer_widgets">
                <div id="footer_widget_left" class="col-md-4">
                    <?php
                    if (is_active_sidebar( 'Footer Left' )) {
                        dynamic_sidebar( 'Footer Left' );
                    } else {
                        if (nimbus_get_option('example_widgets') == "on") {
                        ?>
                            <div class="footer_widget sidebar sidebar_editable">
                                <?php
                                the_widget('WP_Widget_Recent_Posts');
                                ?>
                            </div>
                        <?php
                        }
                    }
                    ?>
                </div>
                <div id="footer_widget_center" class="col-md-4">
                    <?php
                    if (is_active_sidebar( 'Footer Center' )) {
                        dynamic_sidebar( 'Footer Center' );
                    } else {
                        if (nimbus_get_option('example_widgets') == "on") {
                        ?>
                            <div class="footer_widget sidebar sidebar_editable">
                                <?php
                                    $rss_options = array(
                                        'title' => 'WordPress News Feed',
                                        'url' => 'http://wordpress.org/news/feed/',
                                        'items' => 7
                                    );
                                    the_widget('WP_Widget_RSS', $rss_options);
                                ?>
                            </div>
                        <?php
                        }
                    }
                    ?>
                </div>
                <div id="footer_widget_right" class="col-md-4">
                    <?php
                    if (is_active_sidebar( 'Footer Right' )) {
                        dynamic_sidebar( 'Footer Right' );
                    } else {
                        if (nimbus_get_option('example_widgets') == "on") {
                        ?>
                            <div class="footer_widget sidebar sidebar_editable">
                                <?php
                                the_widget( 'WP_Widget_Tag_Cloud');
                                ?>
                            </div>
                        <?php
                        }
                    }
                    ?>
                </div>
            </div>
            <div class="row">
                <div class="col-md-5">
                    <p id="copyright"><?php echo nimbus_get_option('copyright') ?></p>
                </div>
                <div class="col-md-5 col-md-offset-2">
                    <p id="credit"><a href="http://www.nimbusthemes.com/wordpress-themes/simple/">Simple Theme</a> <?php _e('Powered by', 'nimbus'); ?> <a href="http://wordpress.org">WordPress</a></p>
                </div>
            </div>
        </div>
    </div>
<?php wp_footer(); ?>
</body>
</html>