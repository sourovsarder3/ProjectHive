let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()

let loc = window.location
let wsStart = 'ws://'

if (loc.protocol === 'https') {
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function (e) {
    console.log('open')
    send_message_form.on('submit', function (e) {
        e.preventDefault()
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()

        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id
        }
        // console.log(message, send_to, thread_id)
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function (e) {
    console.log('message')
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    // console.log(message, sent_by_id, thread_id)
    console.log(data)
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function (e) {
    console.log('error')
}

socket.onclose = async function (e) {
    console.log('close')
}


function newMessage(message, sent_by_id, thread_id) {
    if ($.trim(message) === '') {
        return false;
    }
    let message_element;
    let chat_id = 'chat_' + thread_id
    if (sent_by_id == USER_ID) {
        message_element = `
			<div class="d-flex mb-4 replied">
				<div class="msg_cotainer_send">
					${message}
					<span class="msg_time_send">8:55 AM, Today</span>
				</div>
				<div class="img_cont_msg">
					<img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg">
				</div>
			</div>
	    `
    }
    else {
        message_element = `
           <div class="d-flex mb-4 received">
              <div class="img_cont_msg">
                 <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg">
              </div>
              <div class="msg_cotainer">
                 ${message}
              <span class="msg_time">8:40 AM, Today</span>
              </div>
           </div>
        `

    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
    message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
    input_message.val(null);
}


$('.contact-li').on('click', function () {
    $('.contacts .active').removeClass('active')
    $('.channel .active').removeClass('active')
    $(this).addClass('active')

    // message wrappers
    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id + '"]').addClass('is_active')
    console.log(chat_id)

})

$('.msg-box').on('click', function () {
    $('.card-body.notification_body.is_active').removeClass('is_active')
    $('.card-body.contacts_body.hide').addClass('is_active')
    $('.menu_body.hide.is_active').removeClass('is_active')
})

$('.notification-box').on('click', function () {
    $('.card-body.contacts_body.is_active').removeClass('is_active')
    $('.card-body.notification_body.hide').addClass('is_active')
    $('.menu_body.hide.is_active').removeClass('is_active')
})

var clicks = true;
$('#action_menu_btn').click(function () {
    if (clicks) {
        $('.action_menu.hide').addClass('is_active');
        $('.menu_body.hide.is_active').removeClass('is_active')
        clicks = false;
    } else {
        $('.action_menu.hide.is_active').removeClass('is_active')
        $('.menu_body.hide.is_active').removeClass('is_active')
        clicks = true;
    }
});

var clicks = true;
$('.menu-box').click(function () {
    if (clicks) {
        $('.menu_body.hide').addClass('is_active');
        $('.action_menu.hide.is_active').removeClass('is_active')
        clicks = false;
    } else {
        $('.menu_body.hide.is_active').removeClass('is_active')
        $('.action_menu.hide.is_active').removeClass('is_active')
        clicks = true;
    }
});


var toggle_clicks = true;
$('.contact_toggle').click(function () {
    if (toggle_clicks) {
        $('.contacts.hide.is_active').removeClass('is_active');
        toggle_clicks = false;
    } else {
        $('.contacts.hide').addClass('is_active')
        toggle_clicks = true;
    }
});

var channel_toggle_clicks = true;
$('.channel_toggle').click(function () {
    if (channel_toggle_clicks) {
        $('.channel.hide.is_active').removeClass('is_active');
        channel_toggle_clicks = false;
    } else {
        $('.channel.hide').addClass('is_active')
        channel_toggle_clicks = true;
    }
});

function get_active_other_user_id() {
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id() {
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}

const searchInput = document.getElementById("search-input");
const dataList = document.getElementById("data-list");
const dataItems = dataList.getElementsByTagName("li");

searchInput.addEventListener("keyup", function () {
    const searchTerm = this.value.toLowerCase();
    Array.from(dataItems).forEach(function (item) {
        const itemText = item.textContent.toLowerCase();
        if (searchTerm === ' ' || searchTerm === '') {
            item.style.display = "none";
        } else if (itemText.indexOf(searchTerm) !== -1) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    });
});





let file = input_file.files[0]
let fileReader = new FileReader()
fileReader.readAsDataURL(file)
fileReader.onload = function () {
    let base64ImageString = fileReader.result

    let data = {
        'message': message,
        'sent_by': USER_ID,
        'send_to': send_to,
        'thread_id': thread_id,
        'is_channel': is_channel,
        'file': base64ImageString
    }
    data = JSON.stringify(data)
    socket.send(data)
}
$(this)[0].reset()


socket.onopen = async function (e) {
    console.log('open')
    send_message_form.on('submit', function (e) {
        e.preventDefault()
        console.log("Submitted")
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let is_channel = check_is_channel()
        let thread_id = get_active_thread_id()

        // Convert image file to base64 string
        let file = input_file.files[0]
        let fileReader = new FileReader()
        fileReader.readAsDataURL(file)
        fileReader.onload = function () {
            let base64ImageString = fileReader.result

            let data = {
                'message': message,
                'sent_by': USER_ID,
                'send_to': send_to,
                'thread_id': thread_id,
                'is_channel': is_channel,
                'file': base64ImageString
            }
            data = JSON.stringify(data)
            socket.send(data)
        }
        $(this)[0].reset()
    })
}
