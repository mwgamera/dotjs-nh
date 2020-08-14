"use strict"

let queue = []
let port = chrome.runtime.connectNative("klg.dotjs_nh")
port.onMessage.addListener(msg => queue.shift()(msg))

chrome.webNavigation.onCommitted.addListener(details => {
  port.postMessage(details.url)
  queue.push(msg => {
    if (msg[1]) msg[1].forEach(code =>
      chrome.tabs.insertCSS(details.tabId, {
        code, frameId: details.frameId,
        runAt: "document_start"
      }))
    if (msg[0]) msg[0].forEach(code =>
      chrome.tabs.executeScript(details.tabId, {
        code, frameId: details.frameId,
        runAt: "document_end"
      }))
  })
})
