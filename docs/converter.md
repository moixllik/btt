[Home](/btt/) |
[Download](/btt/download) |
[Converter](/btt/converter) |
[Support](https://github.com/moixllik/btt/issues)

---

## Convert to BTT

<form onsubmit="return false;">
    <label>
      <input type="file" name="source" accept=".srt,.vtt" onchange="onConvert(this)">
    </label>
    <button type="button" onclick="onCopy(this)">Copy</button>
    <button type="button" onclick="onDownload(this)">Download</button>
    <textarea name="result" rows="7" placeholder="BTT"></textarea>
</form>
<script>
    function onConvert(elm) {
      const form = elm.parentNode.parentNode
      const file = form.source.files[0]
      const reader = new FileReader()
      reader.onload = function (e) {
        const content = e.target.result
        subtitlesToBtt(form.result, content)
      }
      if (file) reader.readAsText(file)
    }

    function formatBtt(start, end, text) {
      return `start=${start}+0;\nend=${end}+0;\n${text}\n`
    }

    function subtitlesToBtt(output, content) {
      let result = []
      let timer = []
      let text = ''
      for (const line of content.split('\n')) {
        if (line.includes(' --> ')) {
          timer = line.match(/\d+:\d+:\d+/g)
          continue
        }
        if (timer.length == 2 && line.length > 0) {
          text = line
          continue
        }
        if (timer.length == 2 && text.length > 0) {
          result.push(formatBtt(timer[0], timer[1], text))
          timer = []
          text = ''
        }
      }
      if (timer.length == 2 && text.length > 0) {
        result.push(formatBtt(timer[0], timer[1], text))
      }
      output.value = result.join('\n')
    }

    function onCopy(elm) {
      const form = elm.parentNode
      form.result.select()
      form.result.setSelectionRange(0, 99999)
      document.execCommand('copy')
    }

    function onDownload(elm) {
      const form = elm.parentNode
      const blob = new Blob([form.result.value], { type: 'text/plain' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = 'subtitles.btt'
      link.click()
      URL.revokeObjectURL(link.href)
    }
</script>
<style>
    textarea {
      display: block;
      width: 100%;
    }

    label {
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: var(--background);
      border-radius: 5px;
      height: 80px;
    }

    input {
      outline: none;
      width: fit-content;
    }
</style>
