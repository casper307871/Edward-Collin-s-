// server.js
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static('public'));

// Simple in-memory role tracking:
let broadcasterSocketId = null;

io.on('connection', (socket) => {
  console.log('conn', socket.id);

  // broadcaster announces itself
  socket.on('broadcaster', () => {
    broadcasterSocketId = socket.id;
    socket.broadcast.emit('broadcaster-started');
    console.log('broadcaster set', broadcasterSocketId);
  });

  // viewer asks for broadcaster
  socket.on('viewer', () => {
    if (broadcasterSocketId) {
      io.to(broadcasterSocketId).emit('viewer', socket.id);
    } else {
      socket.emit('no-broadcaster');
    }
  });

  // signaling: offer/answer/ice candidates
  socket.on('offer', (id, description) => {
    io.to(id).emit('offer', socket.id, description);
  });

  socket.on('answer', (id, description) => {
    io.to(id).emit('answer', socket.id, description);
  });

  socket.on('candidate', (id, candidate) => {
    io.to(id).emit('candidate', socket.id, candidate);
  });

  socket.on('stop-broadcast', () => {
    if (socket.id === broadcasterSocketId) {
      broadcasterSocketId = null;
      socket.broadcast.emit('broadcaster-stopped');
    }
  });

  socket.on('disconnect', () => {
    if (socket.id === broadcasterSocketId) {
      broadcasterSocketId = null;
      socket.broadcast.emit('broadcaster-stopped');
    }
    console.log('disconnect', socket.id);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Listening on ${PORT}`));
