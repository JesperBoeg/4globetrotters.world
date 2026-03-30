<?php
if (nimbus_get_option('example_widgets') == "on") {
    the_widget('WP_Widget_Calendar');
    the_widget('WP_Widget_Categories');
    the_widget( 'WP_Widget_Meta' );
}
?>