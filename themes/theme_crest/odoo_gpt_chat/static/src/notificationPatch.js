/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
import { MainComponentsContainer } from "@web/core/main_components_container"
import { session } from "@web/session";
import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";

const { onMounted } = owl;

patch(MainComponentsContainer.prototype, {
    setup() {
        super.setup(...arguments);
        this.httpService = useService("http");
        const body = document.getElementsByTagName('head')[0];
        this.action = useService("action");

        onMounted(async () => {
            const chatbot = await rpc("/get/chatbot");
            const body = document.body || document.head;
            if (!chatbot) {
                // 🔹 Create clickable chatbot disabled message
                const fallback = document.createElement("div");
                fallback.className = "chatbot-disabled-msg";
                fallback.style.cssText = `
                        position: fixed;
                        bottom: 25px;
                        right: 30px;
                        background: #141b38;
                        color: #ffffffff;
                        height: 60px;
                        width : 60px;
                        border-radius: 50%;
                        display:flex;
                        justify-content:center;
                        align-items:center;
                        font-size: 22px;
                        z-index: 9999;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
                        cursor: pointer;
                        transition: all 0.3s ease;
                    `;
                fallback.innerHTML = `<img src="/odoo_gpt_chat/static/img/logo1.webp" title="logo" alt="logo"  style="border-radius: 50%;" class=" w-100 h-100">`;  // ✅ fixed icon
                body.appendChild(fallback);

                // Create hidden popup
                const popup = document.createElement("div");
                popup.className = "chatbot-disabled-popup";
                popup.style.cssText = `
                        display: none;
                        position: fixed;
                        bottom: 95px;
                        right: 35px;
                        background: #fff;
                        color: #333;
                        border: 1px solid #ccc;
                        height:750px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                        z-index: 10000;
                        font-size: 13px;
                        width: 440px;
                    `;
                popup.innerHTML = ` 
                        <div class="chatbot-main h-100 justify-content-between d-flex flex-column">
                            <div class="d-flex justify-content-between align-items-center" style="background: #141B38; color: #ffffffff; border-radius: 8px 8px 0 0; padding:10px 15px;">
                                <h5 class="mb-0 d-flex align-items-center " style="color: white; font-size: 18px">
                                    <img src="/odoo_gpt_chat/static/img/logo1.webp" title="logo" alt="logo"  style="border-radius: 50%;" class="me-2">
                                    Whisperchat
                                </h5>
                                <i class="oi oi-close close-chat" aria-hidden="true" style="font-size:18px; cursor: pointer;"></i>
                            </div>
                            <div class="text-center">
                                <p class="px-3 text-center" style="font-size: 16px; font-weight: 500;">Make your Odoo store smarter in 5 minutes with WhisperChat.ai.
                                    Build a chatbot that answers questions, captures leads, and keeps customers engaged - no coding needed.</p>
                                <p class="px-3 text-center mt-3" style="font-size: 16px; font-weight: 500;">Sign up at <a href="https://www.whisperchat.ai/" style="font-weight: 900; color: #141B38;"> whisperchat.ai </a>, create a bot, and connect it inside <a style="font-weight: 900; color: #141B38; cursor: pointer;" class="open-odoo-settings"> Odoo </a> Learn more at <a href="https://apps.odoo.com/apps/modules/18.0/odoo_gpt_chat#desc" style="font-weight: 900; color: #141B38; word-wrap:break-word; text-decoration: underline;"> https://apps.odoo.com/apps/modules/18.0/odoo_gpt_chat#desc </a></p>
                            </div>
                            <div class="d-flex  mb-2 flex-column   align-items-center">
                                <div class="px-3 w-100 position-relative">
                                    <input type="text" class="w-100" style="border-radius: 8px; background: white; border: 1px solid #141B38; padding: 10px 10px" placeholder="Message"/>
                                    <i class="fa fa-paper-plane-o position-absolute" style="top: 50%; right: 33px; transform: translateY(-50%); font-size: 16px; cursor: pointer;" aria-hidden="true"></i>
                                </div>
                                <p class="mb-0 mt-2" style="color: black"> Powered by <a href="https://www.whisperchat.ai/"  class=" fw-bold" style="color: black"> whisperchat.ai</a></p>
                            </div>
                        </div>
                    `;
                body.appendChild(popup);
                const openSettings = popup.querySelector(".open-odoo-settings");
                openSettings.addEventListener("click", () => {
                    // ✅ Open action for Settings (res.config.settings)
                    this.action.doAction({
                        type: "ir.actions.act_window",
                        res_model: "res.config.settings",
                        views: [[false, "form"]],
                        target: "current",
                        name: "Settings",
                    });
                });

                const closeBtn = popup.querySelector('.close-chat');
                if (closeBtn) {
                    closeBtn.addEventListener('click', () => {
                        popup.style.display = 'none';
                    });
                }
                // Toggle popup on click
                fallback.addEventListener("click", () => {
                    popup.style.display =
                        popup.style.display === "none" ? "block" : "none";
                });

                return;
            }
            if (chatbot) {
                const script = document.createElement("script");
                // script.id = "whisperchat-ai";
                script.type = "text/javascript";
                script.src = "https://widget.whisperchat.ai/embed.js";
                script.id = chatbot.id;
                // // script.defer = true;
                const chatScript = document.getElementById(chatbot);
                if (chatScript && chatScript.length > 0) {
                    return;
                } else {
                    if (chatbot.front_end && chatbot.back_end) {
                        if (session.is_frontend) {
                            if (window.self !== window.top) {
                                return;
                            } else {
                                body.appendChild(script);
                            }
                        } else {
                            body.appendChild(script);
                        }
                    } else {
                        if (chatbot.front_end) {
                            if (session.is_frontend) {
                                body.appendChild(script);
                            }
                        }
                        if (chatbot.back_end) {
                            if (!Boolean(session.is_frontend)) {
                                body.appendChild(script);
                            }
                        }
                    }

                }
            }
        })
    },
})