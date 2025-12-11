const go = document.getElementById("go");
      const topicEl = document.getElementById("topic");
      const topEl = document.getElementById("top");
      const bottomEl = document.getElementById("bottom");
      const resultDiv = document.getElementById("result");
      const captionEl = document.getElementById("caption");
      const memeImg = document.getElementById("meme");

      go.onclick = async () => {
        const topic = topicEl.value.trim();
        if (!topic) return alert("Enter a topic.");
        go.disabled = true;
        go.textContent = "Generating... (this may take a few seconds)";

        try {
          const resp = await fetch("http://localhost:8000/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              topic,
              top_text: topEl.value || undefined,
              bottom_text: bottomEl.value || undefined,
            }),
          });

          if (!resp.ok) {
            const err = await resp.json().catch(() => null);
            throw new Error(
              err?.detail || resp.statusText || "Generation failed"
            );
          }

          const data = await resp.json();
          const { caption, image_b64 } = data;
          captionEl.textContent = caption || "";
          memeImg.src = "data:image/png;base64," + image_b64;
          resultDiv.style.display = "block";
        } catch (e) {
          alert("Error: " + (e.message || e));
          console.error(e);
        } finally {
          go.disabled = false;
          go.textContent = "Generate Meme";
        }
      };

      downloadBtn.onclick = () => {
        const imageURL = memeImg.src;
        const a = document.createElement("a");
        a.href = imageURL;
        a.download = "meme.png"; // filename
        a.click();
      };