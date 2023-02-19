const switch2Polygon = async (library) => {
  try {
    await library.provider.request({
      method: "wallet_switchEthereumChain",
      params: [{ chainId: "0x89" }], // hex of 137, polygon mainnet
    });
  } catch (switchError) {
    // 4902 error code indicates the chain is missing on the wallet
    if (switchError.code === 4902) {
      try {
        await library.provider.request({
          method: "wallet_addEthereumChain",
          params: [
            {
              chainId: "0x89",
              rpcUrls: ["https://rpc.ankr.com/polygon"],
              chainName: "Polygon Mainnet",
              nativeCurrency: { name: "Matic", decimals: 18, symbol: "MATIC" },
              blockExplorerUrls: ["https://polygonscan.com"],
              iconUrls: ["https://polygon.technology/_nuxt/img/polygon-logo-2023.2dfe51d.svg"]
            }
          ],
        });
      } catch (error) {
        console.error(error)
      }
    }
  }
};
export { switch2Polygon};

