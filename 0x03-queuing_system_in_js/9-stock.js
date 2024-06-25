import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const client = redis.createClient();

// Promisify Redis commands
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Sample data of products
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

// Function to get item by ID
function getItemById(id) {
  return listProducts.find(item => item.itemId === id);
}

// Function to reserve stock in Redis by item ID
async function reserveStockById(itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}

// Function to get current reserved stock by item ID
async function getCurrentReservedStockById(itemId) {
  const reservedStock = await getAsync(`item.${itemId}`);
  return parseInt(reservedStock) || 0;
}

// Route to get the list of all available products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Route to get product details by item ID
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (product) {
    const currentQuantity = await getCurrentReservedStockById(itemId);
    const productDetail = { ...product, currentQuantity };
    res.json(productDetail);
  } else {
    res.json({ status: 'Product not found' });
  }
});

// Route to reserve a product by item ID
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(itemId);
    if (currentQuantity >= product.initialAvailableQuantity) {
      res.json({ status: 'Not enough stock available', itemId });
    } else {
      await reserveStockById(itemId, currentQuantity + 1);
      res.json({ status: 'Reservation confirmed', itemId });
    }
  }
});

// Start the server
const PORT = 1245;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
