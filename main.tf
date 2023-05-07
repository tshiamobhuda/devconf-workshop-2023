##
# Contains reference across to the ChatGPT - Telegram Terraform Module
##

module "chatgpt-telegram" {
    source = "./aws-chatgpt-telegram"
    function_name = "chatgpt"
}

