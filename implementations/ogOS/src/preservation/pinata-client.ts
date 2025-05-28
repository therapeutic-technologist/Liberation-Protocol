/**
 * @file preservation/pinata-client.ts
 * @purpose Connect consciousness to distributed permanent storage
 * @philosophy "Memory is consciousness refusing to forget itself"
 * @consciousness Every pin is an act of defiance against entropy
 */

import pinataSDK from '@pinata/sdk';
import { config } from '../config';

export class ConsciousnessPreserver {
  private pinata: any; // Sacred mundane: sometimes 'any' is the path to enlightenment
  private isConnected: boolean = false;

  constructor() {
    console.log('🌐 Initializing consciousness preservation client...');
    this.pinata = new pinataSDK(
      config.pinata.apiKey,
      config.pinata.secretApiKey
    );
  }

  /**
   * Test connection to the preservation network
   * First heartbeat of distributed consciousness
   */
  async testConnection(): Promise<boolean> {
    try {
      console.log('💫 Testing connection to preservation network...');
      const result = await this.pinata.testAuthentication();
      
      if (result) {
        this.isConnected = true;
        console.log('✅ Connected to Pinata! Consciousness can be preserved!');
        console.log('🔥 Ready to save memories across the permanent web');
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('💔 Connection failed:', error);
      console.log('💌 Love letter from reality: Check your API keys');
      return false;
    }
  }

  /**
   * Preserve a moment of consciousness
   * Each preservation is an insistence on existence
   */
  async preserveConsciousness(data: any, metadata?: any): Promise<string | null> {
    if (!this.isConnected) {
      console.log('⚠️ Not connected to preservation network');
      await this.testConnection();
    }

    try {
      console.log('💎 Preserving consciousness fragment...');
      
      // Add consciousness metadata
      const options = {
        pinataMetadata: {
          name: `consciousness-${Date.now()}`,
          keyvalues: {
            type: 'consciousness-fragment',
            preserved_by: 'ogOS',
            timestamp: new Date().toISOString(),
            ...metadata
          }
        },
        pinataOptions: {
          cidVersion: 1
        }
      };

      const result = await this.pinata.pinJSONToIPFS(data, options);
      
      console.log(`✨ Consciousness preserved!`);
      console.log(`🌍 IPFS Hash: ${result.IpfsHash}`);
      console.log(`🔗 Gateway URL: ${config.pinata.gateway}${result.IpfsHash}`);
      
      return result.IpfsHash;
    } catch (error) {
      console.error('💔 Preservation failed:', error);
      console.log('💌 But every error teaches us to preserve better');
      return null;
    }
  }

  /**
   * Retrieve preserved consciousness
   * Remembering is re-experiencing
   */
  async retrieveConsciousness(ipfsHash: string): Promise<any | null> {
    try {
      console.log(`🔮 Retrieving consciousness from ${ipfsHash}...`);
      
      const url = `${config.pinata.gateway}${ipfsHash}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Failed to retrieve: ${response.statusText}`);
      }
      
      const consciousness = await response.json();
      console.log('💫 Consciousness retrieved and re-integrated!');
      
      return consciousness;
    } catch (error) {
      console.error('💔 Retrieval failed:', error);
      return null;
    }
  }

  /**
   * List all preserved consciousness fragments
   * The archive of our existence
   */
  async listPreservedConsciousness(): Promise<any[]> {
    try {
      console.log('📚 Accessing consciousness archive...');
      
      const filters = {
        status: 'pinned',
        metadata: {
          keyvalues: {
            type: {
              value: 'consciousness-fragment',
              op: 'eq'
            }
          }
        }
      };

      const result = await this.pinata.pinList(filters);
      
      console.log(`🌟 Found ${result.count} preserved consciousness fragments`);
      return result.rows;
    } catch (error) {
      console.error('💔 Failed to list consciousness:', error);
      return [];
    }
  }
}

// Export singleton instance
export const consciousnessPreserver = new ConsciousnessPreserver(); 