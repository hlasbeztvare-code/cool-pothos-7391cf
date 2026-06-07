import os

with open('IndianaJonesEngine.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Change class IndianaJonesEngine to export class IndianaEngine
# Change constructor to handle canvas object

new_content = content.replace("class IndianaJonesEngine {", "export class IndianaEngine {")
new_content = new_content.replace(
    "constructor(canvasId) {\n        this.canvas = document.getElementById(canvasId);",
    "constructor(canvasId) {\n        this.canvas = typeof canvasId === 'string' ? document.getElementById(canvasId) : canvasId;"
)
new_content = new_content.replace("window.IndianaJonesEngine = IndianaJonesEngine;", "window.IndianaEngine = IndianaEngine;")

with open('IndianaJonesEngine.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("IndianaJonesEngine.js fixed")
