function saveNote() {
    const noteInput = document.getElementById('note-input');
    const notesList = document.getElementById('notes-list');

    const noteText = noteInput.value;
    if (noteText.trim() !== '') {
        fetch('/add_note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `note=${noteText}`
        })
        .then(response => response.json())
        .then(data => {
            renderNotes(data.notes);
            noteInput.value = '';
        });
    }
}

function deleteNote(noteText) {
    fetch('/delete_note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `note=${noteText}`
    })
    .then(response => response.json())
    .then(data => {
        renderNotes(data.notes);
    });
}

function renderNotes(notes) {
    const notesList = document.getElementById('notes-list');
    notesList.innerHTML = '';
    notes.forEach(noteText => {
        const note = document.createElement('div');
        note.className = 'note';

        const noteContent = document.createElement('div');
        noteContent.className = 'note-content';
        noteContent.textContent = noteText;

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = function() {
            deleteNote(noteText);
        };

        note.appendChild(noteContent);
        note.appendChild(deleteBtn);

        notesList.appendChild(note);
    });
}
