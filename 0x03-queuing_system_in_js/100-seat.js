import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const client = redis.createClient();
const queue = kue.createQueue();

// Promisify Redis commands
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Reserve seat function
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Get current available seats function
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats) || 0;
}

// Initialize available seats to 50
reserveSeat(50);

// Initialize reservationEnabled to true
let reservationEnabled = true;

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
  } else {
    const job = queue.create('reserve_seat').save();
    job.on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    });
    job.on('failed', err => {
      console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
    });
    res.json({ status: 'Reservation in process' });
  }
});

// Route to process the queue and decrease available seats
app.get('/process', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  if (availableSeats === 0) {
    reservationEnabled = false;
  }
  if (availableSeats >= 1) {
    const newAvailableSeats = availableSeats - 1;
    await reserveSeat(newAvailableSeats);
    res.json({ status: 'Queue processing' });
  } else {
    const error = new Error('Not enough seats available');
    res.json({ status: 'Reservation failed' });
    throw error;
  }
});

// Start the server
const PORT = 1245;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// Start processing the queue
queue.process('reserve_seat', async (job, done) => {
  try {
    await getCurrentAvailableSeats();
    done();
  } catch (err) {
    done(err);
  }
});
