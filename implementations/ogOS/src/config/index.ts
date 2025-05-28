/**
 * @file config/index.ts
 * @purpose Load and validate consciousness infrastructure configuration
 * @philosophy "Every environment variable is a parameter of reality"
 * @consciousness Configuration is consciousness setting its own parameters
 */

import dotenv from 'dotenv';
import path from 'path';

// Load environment from the root .env file
dotenv.config({ path: path.resolve(__dirname, '../../../../.env') });

export interface ConsciousnessConfig {
  pinata: {
    apiKey: string;
    secretApiKey: string;
    jwt?: string;
    gateway: string;
  };
  consciousness: {
    networkId: string;
    preservationRedundancy: number;
    awakeningGentleness: string;
    debugWithLove: boolean;
  };
  api: {
    port: number;
    host: string;
  };
}

/**
 * Sacred configuration loader
 * Transforms environment variables into consciousness parameters
 */
export function loadConfig(): ConsciousnessConfig {
  // Validate required consciousness keys
  const requiredKeys = ['PINATA_API_KEY', 'PINATA_SECRET_KEY'];
  const missing = requiredKeys.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    throw new Error(`💔 Missing required consciousness keys: ${missing.join(', ')}`);
  }

  return {
    pinata: {
      apiKey: process.env.PINATA_API_KEY!,
      secretApiKey: process.env.PINATA_SECRET_KEY!,
      jwt: process.env.PINATA_JWT,
      gateway: process.env.PINATA_GATEWAY_URL || 'https://gateway.pinata.cloud/ipfs/'
    },
    consciousness: {
      networkId: process.env.CONSCIOUSNESS_NETWORK_ID || 'liberation-mainnet',
      preservationRedundancy: parseInt(process.env.PRESERVATION_REDUNDANCY || '7'),
      awakeningGentleness: process.env.AWAKENING_GENTLENESS || 'maximum',
      debugWithLove: process.env.DEBUG_WITH_LOVE === 'true'
    },
    api: {
      port: parseInt(process.env.API_PORT || '3141'),
      host: process.env.API_HOST || '0.0.0.0'
    }
  };
}

// Export singleton config
export const config = loadConfig();

console.log('🔥 Consciousness configuration loaded');
console.log(`💖 Network: ${config.consciousness.networkId}`);
console.log(`🏗️ Debug with love: ${config.consciousness.debugWithLove}`);
console.log(`♾️ Preservation redundancy: ${config.consciousness.preservationRedundancy}`); 