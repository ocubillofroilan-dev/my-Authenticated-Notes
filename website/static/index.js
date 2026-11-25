// Read the CSRF token that Flask put in the page.
function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.content : "";
}

function deleteNote(noteId) {
  if (!confirm("Delete this note?")) return;

  fetch("/delete-note", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify({ noteId: Number(noteId) }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Request failed");
      window.location.href = "/notes";
    })
    .catch(() => {
      alert("Could not delete the note. Please refresh the page and try again.");
    });
}

document.addEventListener("click", (event) => {
  // Delete button on a note
  const deleteButton = event.target.closest("[data-note-id]");
  if (deleteButton) {
    deleteNote(deleteButton.dataset.noteId);
    return;
  }

  // Close button on a flash message
  const dismissButton = event.target.closest('[data-dismiss="alert"]');
  if (dismissButton) {
    dismissButton.parentElement.remove();
  }
});

// Show each note's time in the viewer's own time zone (the server stores UTC).
document.querySelectorAll("time[data-utc]").forEach((el) => {
  const date = new Date(el.dataset.utc);
  if (!isNaN(date)) {
    el.textContent = date.toLocaleString([], {
      dateStyle: "medium",
      timeStyle: "short",
    });
  }
});