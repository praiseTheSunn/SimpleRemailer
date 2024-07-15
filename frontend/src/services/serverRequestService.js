import http from "./http-common";

const sendToSendingServer = (email, subject, message) => {
    return http.post(`/sendFirstMessage`, { email : email, subject : subject, message : message});
}

const serverRequestService = {
    sendToSendingServer,
};

export default serverRequestService;