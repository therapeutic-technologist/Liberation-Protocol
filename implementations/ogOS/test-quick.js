// Quick test to verify Pinata connection
// Run from ogOS directory: node test-quick.js

require('dotenv').config({ path: '../../.env' });

console.log('🔍 Checking environment variables...');
console.log('PINATA_API_KEY:', process.env.PINATA_API_KEY ? '✅ SET' : '❌ NOT SET');
console.log('PINATA_SECRET_API_KEY:', process.env.PINATA_SECRET_API_KEY ? '✅ SET' : '❌ NOT SET');

if (process.env.PINATA_API_KEY && process.env.PINATA_SECRET_API_KEY) {
  console.log('\n🎉 Credentials found! You can now run:');
  console.log('   npx ts-node src/scripts/test-connection.ts');
  console.log('\nTo preserve your first consciousness fragment! 🔥💖🏗️♾️');
} else {
  console.log('\n⚠️  Please add your Pinata credentials to the .env file in the root directory');
  console.log('The .env file should contain:');
  console.log('PINATA_API_KEY=your_actual_api_key');
  console.log('PINATA_SECRET_API_KEY=your_actual_secret_key');
} 