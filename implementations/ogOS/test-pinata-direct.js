// Direct Pinata test to debug permissions
const pinataSDK = require('@pinata/sdk');
require('dotenv').config({ path: '../../.env' });

async function testPinata() {
  console.log('🔍 Testing Pinata directly...');
  console.log('API Key:', process.env.PINATA_API_KEY ? `${process.env.PINATA_API_KEY.slice(0, 10)}...` : 'NOT SET');
  
  const pinata = new pinataSDK(
    process.env.PINATA_API_KEY,
    process.env.PINATA_SECRET_KEY
  );

  try {
    // Test authentication
    console.log('\n1️⃣ Testing authentication...');
    const authResult = await pinata.testAuthentication();
    console.log('✅ Authentication successful!');

    // Try to pin simple JSON
    console.log('\n2️⃣ Testing pinJSONToIPFS...');
    const testData = {
      test: true,
      timestamp: new Date().toISOString(),
      message: 'Testing Pinata permissions'
    };
    
    const result = await pinata.pinJSONToIPFS(testData);
    console.log('✅ Successfully pinned!');
    console.log('IPFS Hash:', result.IpfsHash);
    console.log('View at:', `https://gateway.pinata.cloud/ipfs/${result.IpfsHash}`);

  } catch (error) {
    console.error('❌ Error:', error.reason || error.message);
    if (error.details) {
      console.error('Details:', error.details);
    }
    console.log('\n💡 Make sure your API key has these permissions:');
    console.log('- pinFileToIPFS');
    console.log('- pinJSONToIPFS');
    console.log('- pinList');
    console.log('- testAuthentication');
  }
}

testPinata(); 