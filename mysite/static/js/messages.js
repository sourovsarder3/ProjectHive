let input_message = $('#input-message')
let input_file = document.querySelector('#file-message');
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()
const myInput = document.getElementById('input-message');




// Listen for changes to the input and handle them
input_file.addEventListener('change', (event) => {
    // Get the selected file
    const file = event.target.files[0];
    console.log(file.size)


    // Create a new FileReader instance
    const reader = new FileReader();

    // Set up an event listener for when the reader has finished reading the file
    reader.addEventListener('load', () => {
        // Get the base64-encoded string of the image data
        const base64ImageString = reader.result;


        // Do something with the string (e.g. send it over a WebSocket)
        // console.log(base64ImageString);
        if (file.size > 10485760) {
            myInput.value = "Maximum file size is 10MB";
        } else {
            myInput.value = file.name;
            console.log('Selected')
        }


    });

    // Read the file as a data URL (which will give us a base64-encoded string)
    reader.readAsDataURL(file);
});






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
        console.log("Submitted")
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let is_channel = check_is_channel()
        let thread_id = get_active_thread_id()
        let file = input_file.files[0]

        if (file != null && file.size < 10485760) {
            console.log('Not Null')
            let str = file.type
            let type_arr = str.split('/');
            let file_type = type_arr[0]

            console.log(file_type)

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
                    'has_file': '1',
                    'file_type': file_type,
                    'file': base64ImageString
                }
                data = JSON.stringify(data)
                socket.send(data)
            }
        } else {
            let data = {
                'message': message,
                'sent_by': USER_ID,
                'send_to': send_to,
                'thread_id': thread_id,
                'is_channel': is_channel,
                'has_file': '0',
                'file_type': null,
                'file': null
            }
            data = JSON.stringify(data)
            socket.send(data)
        }
        $(this)[0].reset()

    })
}

socket.onmessage = async function (e) {
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    let is_channel = data['is_channel']
    let sender_name = data['sender_name']
    let file = data['file']
    let file_type = data['file_type']
    console.log(data)
    // console.log(file)
    newMessage(message, sent_by_id, thread_id, is_channel, sender_name, file, file_type)
}

socket.onerror = async function (e) {
    console.log('error')
}

socket.onclose = async function (e) {
    console.log('close')
}


function newMessage(message, sent_by_id, thread_id, is_channel, sender_name, file, file_type) {
    if ($.trim(message) === '') {
        return false;
    }

    var now = new Date();
    var formattedDate = now.toLocaleString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true
    });


    let message_element;
    let chat_id = 'chat_' + thread_id
    if (sent_by_id == USER_ID) {
        if (file != null) {
            if (file_type == 'image') {
                message_element = `
                    <div class="msg_send">
                        <div class="d-flex mb-4 replied">                        
                            <div class="msg_cotainer_send">                                                                                    
                            <img src="${file}" width= 200px >                                                   
                            </div>                            
                            <div class="img_cont_msg">
                                <img src="http://127.0.0.1:8000/media/DP.jpg" class="rounded-circle user_img_msg">
                            </div>
                        </div>
                        <span class="msg_time_send">${formattedDate}</span>
                    </div>
                `
            } else if (file_type == 'video') {
                message_element = `
                    <div class="msg_send">
                        <div class="d-flex mb-4 replied">                        
                            <div class="msg_cotainer_send">
                                <video width="320" height="240" controls>
                                    <source src="${file}" type="video/mp4">
                                Your browser does not support the video tag.
                                </video>                                                 
                            </div>
                            <div class="img_cont_msg">
                                <img src="http://127.0.0.1:8000/media/DP.jpg" class="rounded-circle user_img_msg">
                            </div>
                        </div>
                        <span class="msg_time_send">${formattedDate}</span>
                    </div>
                `
            } else {
                message_element = `
                    <div class="msg_send">
                        <div class="d-flex mb-4 replied">                        
                            <div class="msg_cotainer_send">
                                <a href="${file}" download>${message}</a>                                                 
                            </div>
                            <div class="img_cont_msg">
                                <img src="http://127.0.0.1:8000/media/DP.jpg" class="rounded-circle user_img_msg">
                            </div>
                        </div>
                        <span class="msg_time_send">${formattedDate}</span>
                    </div>
                `
            }

        } else {
            message_element = `
            <div class="msg_send">
                <div class="d-flex mb-4 replied">                        
                    <div class="msg_cotainer_send">                                                                                    
                        ${message}                                                        
                    </div>
                    <div class="img_cont_msg">
                        <img src="http://127.0.0.1:8000/media/DP.jpg" class="rounded-circle user_img_msg">
                    </div>
                </div>
                <span class="msg_time_send">${formattedDate}</span>
            </div>
	    `
        }

    }
    else {
        if (file != null) {
            if (file_type == 'image') {
                message_element = `
                    <div class="msg_receive">
                        <div class="msg_send_name">${sender_name}</div>
                        <div class="d-flex mb-4 received">
                            <div class="img_cont_msg">
                                <img src="http://127.0.0.1:8000/media/DP.jpg" class="rounded-circle user_img_msg">
                            </div>
                        
                            <div class="msg_cotainer">
                                <img src="${file}" width= 200px > 
                            </div>
                        </div>
                        <span class="msg_time">${formattedDate}</span>
                    </div>
                `
            } else {
                message_element = `
                    <div class="msg_receive">
                        <div class="msg_send_name">${sender_name}</div>
                        <div class="d-flex mb-4 received">
                            <div class="img_cont_msg">
                                <img src="http://127.0.0.1:8000/media/DP.jpg" class="rounded-circle user_img_msg">
                            </div>
                        
                            <div class="msg_cotainer">
                                <a href="${file}" download>${message}</a> 
                            </div>
                        </div>
                        <span class="msg_time">${formattedDate}</span>
                    </div>
                `
            }

        } else {
            message_element = `
                <div class="msg_receive">
                    <div class="msg_send_name">${sender_name}</div>
                    <div class="d-flex mb-4 received">
                        <div class="img_cont_msg">
                            <img src="http://127.0.0.1:8000/media/DP.jpg" class="rounded-circle user_img_msg">
                        </div>
                    
                        <div class="msg_cotainer">
                            ${message}
                        </div>
                    </div>
                    <span class="msg_time">${formattedDate}</span>
                </div>
            `
        }

    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"][is-channel="' + is_channel + '"] .msg_card_body')
    message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
    input_message.val(null);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$('.contact-li').on('click', function () {
    $('.contacts .active').removeClass('active')
    $('.channel .active').removeClass('active')
    $(this).addClass('active')

    // message wrappers
    let chat_id = $(this).attr('chat-id')
    let is_channel = $(this).attr('is-channel')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id + '"][is-channel="' + is_channel + '"]').addClass('is_active')
    var myDiv = $('.messages-wrapper[chat-id="' + chat_id + '"][is-channel="' + is_channel + '"]')
    let thread_id = chat_id.replace('chat_', '')
    $(myDiv).ready(function () {
        console.log('Seen', chat_id, thread_id)
        if (is_channel == '1') {
            $.ajax({
                url: 'update_seen_by/',
                type: 'POST',
                data: {
                    chat_id: thread_id,
                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                success: function (response) {
                    console.log(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        } else {
            console.log('Not Channel')
        }

    });

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
$('.action_menu_btn').click(function () {
    let chat_id = $(this).attr('chat-id')
    let is_channel = $(this).attr('is-channel')
    if (clicks) {
        $('.menu_body.hide.is_active').removeClass('is_active')
        $('.action_menu.is_active').removeClass('is_active')
        $('.action_menu[chat-id="' + chat_id + '"][is-channel="' + is_channel + '"]').addClass('is_active');
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

function check_is_channel() {
    let is_channel = $('.messages-wrapper.is_active').attr('is-channel')
    is_channel = $.trim(is_channel)
    return is_channel
}

function get_active_thread_id() {
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}

// user in workspace

const searchInput = document.getElementById("search-input");
const dataList = document.getElementById("data-list");
const dataItems = dataList.getElementsByTagName("li");

searchInput.addEventListener("keyup", function () {
    const searchTerm = this.value.toLowerCase();
    Array.from(dataItems).forEach(function (item) {
        const itemText = item.textContent.toLowerCase();
        if (itemText.indexOf(searchTerm) !== -1) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    });
});

//user not in workspace
const searchInputAdd = document.getElementById("search-input-add");
const dataListAdd = document.getElementById("data-list-add");
const dataItemsAdd = dataListAdd.getElementsByTagName("li");

searchInputAdd.addEventListener("keyup", function () {
    const searchTerm = this.value.toLowerCase();
    Array.from(dataItemsAdd).forEach(function (item) {
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

// Add Chennel Member
const searchInputChannel = document.getElementById("search-input-channel");
const dataListChannel = document.getElementById("data-list-channel");
const dataItemsChannel = dataListChannel.getElementsByTagName("li");

searchInputChannel.addEventListener("keyup", function () {
    const searchTerm = this.value.toLowerCase();
    Array.from(dataItemsChannel).forEach(function (item) {
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

// Search File portion
const searchInputfile = document.getElementById("search-input-file");
const dataListfile = document.getElementById("data-list-file");
const dataItemsfile = dataListfile.getElementsByTagName("li");

searchInputfile.addEventListener("keyup", function () {
    const searchTerm = this.value.toLowerCase();
    Array.from(dataItemsfile).forEach(function (item) {
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
