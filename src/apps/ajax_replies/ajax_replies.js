var AJAX_GET_REPLIES_BACKEND = "";
var PAGES_SEPARATOR = " ";

var html_ids = new Array ();

html_ids [ 'feedback_block' ] = 'ajax_replies_feedback_block';
html_ids [ 'replies_block'  ] = 'ajax_replies_block';
html_ids [ 'reply_body'     ] = 'id_body';

var html_names = new Array ();

html_names [ 'pagination_block' ] = 'ajax_replies_pagination_block';

var css_classes = new Array ();

css_classes [ 'feedback_success' ] = 'ajax_feedback_success';
css_classes [ 'feedback_error'   ] = 'ajax_feedback_error';

var feedback = function ( text, is_success ) {
	var fb = $( '#' + html_ids [ 'feedback_block' ] );
    fb.removeClass ();
    if ( is_success )
        fb.addClass ( css_classes [ 'feedback_success' ] );
    else
        fb.addClass ( css_classes [ 'feedback_error' ] );
    fb.html ( text );
};

// convert back-end's error code to error message
var error_handler = function ( error_code ) {
	var error_msg = "Неизвестная ошибка";
    if      ( error_code == 1 )
        error_msg =  "Объект не существует";
    else if ( error_code == 2 )
        error_msg = "Страница не существует";
    else if ( error_code == 3 )
        error_msg = "Пожалуйста, введите текст отзыва";
    else if ( error_code == 4 )
        error_msg = "Вы не можете комментировать данный объект";
    feedback ( error_msg );
};

var render_page = function ( replies, pages_count, page_num ) {
    pages = new Array ()
    // generate array of pages
    for ( var i = 0; i < pages_count; i++ ) {
        if ( i + 1 == page_num )
            pages.push ( i + 1 );
        else
            pages.push ( '<a href="#replies_page' + ( i + 1 ) + '" onclick="get_replies_at_page ( ' + ( i + 1 ) + ', \'' + AJAX_GET_REPLIES_BACKEND + '\' )">' + ( i + 1 ) + '</a>' )
    }
    // fill pagination blocks with pages
    if ( pages.length > 1 )
        $("[name=" + html_names [ 'pagination_block' ] + "]").html ( pages.join ( PAGES_SEPARATOR ) );
    // fill replies block with replies
    $( '#' + html_ids [ 'replies_block' ] ).html ( replies.join ( "" ) );
};

// get replies request to back-end
function get_replies_at_page ( page_num, backend_url ) {
	AJAX_GET_REPLIES_BACKEND = backend_url
	$.get (
        backend_url,
        { page_num : page_num },
        function ( res ) {
            if ( !res.error_code )
                render_page ( res.replies, res.pages_count, res.page_num );
            else
                error_handler ( res.error_code );
        },
        "json"
    );
};    

// add reply request to back-end
function add_reply ( event, backend_url ) {
	event.preventDefault ();
	var reply_body = $( '#' + html_ids [ 'reply_body' ] );
    $.post (
        backend_url,
        { body : reply_body.val () },
        function ( res ) {
            if ( !res.error_code ) {
                reply_body.val ( "" );
                render_page ( res.replies, res.pages_count, res.page_num );
                feedback ( "Коментарий добавлен", true );
            }
            else {
                error_handler ( res.error_code );
            }
        },
        "json"
    );
    feedback ( "Пожалуйста, подождите...", true );
}