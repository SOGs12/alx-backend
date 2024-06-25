import { createClient } from 'redis';

function connectToRedis() {
  const client = createClient();

  client.on('connect', function() {
    console.log('Redis client connected to the server');
  }).on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err}`);
  });

};

connectToRedis();
