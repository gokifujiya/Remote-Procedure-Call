const net = require("net");
const fs = require("fs");
const path = "./socket_file";

// Example request
const request = {
    method: "reverse",
    params: ["Hello"],
    param_types: ["string"],
    id: 1
};

const client = net.createConnection(path, () => {
    client.write(JSON.stringify(request));
});

client.on("data", (data) => {
    const response = JSON.parse(data.toString());
    console.log("Server response:", response);
    client.end();
});
