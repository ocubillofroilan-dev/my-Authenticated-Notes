function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: Number(noteId) }), 
    }).then((_res) => {
        window.location.href = "/";
    });
  }