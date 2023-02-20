import React, { useState, useEffect } from 'react';
import { useWeb3React } from '@web3-react/core';
import { InjectedConnector } from '@web3-react/injected-connector';
import { switch2Polygon} from '../../utils/networkConnect.js';
import Button from '../Buttons/Button.js';
import Modal from '../Modal/Modal.js';
import styles from './Home.module.css'
// logos
import ethereum_icon from '../../icons/ethereum.svg';
import wallet_connect_icon from '../../icons/wallet_connect.svg';

const POLYGON_CHAIN_ID = 137;

export default function Home(props) {
  const [showModal, setShowModal] = useState(false);
  const { activate, deactivate, active, account, library } = useWeb3React();
  
  const injected = new InjectedConnector({
    supportedChainIds: [1, 3, 4, 5, 42, 137],
  })

  async function connectBrowserWallet() {
    try {
      console.log("HERE#####");
      await activate(injected);
      localStorage.setItem('isBrowserWalletConnected', true);
      setShowModal(false);
      props.changePage("form");
    } catch (ex) {
      console.log(ex);
    }
  }

  useEffect(() => {
    const connectWalletOnPageLoad = async () => {
      if (localStorage?.getItem('isBrowserWalletConnected') === 'true') {
        try {
          await activate(injected)
        } catch (ex) {
          console.log(ex)
        }
      }
    }
    connectWalletOnPageLoad()
    console.log(window.ethereum.networkVersion);
  }, [])

  return (
    <div className={styles["main-text"]}>
      <h1>Launch your Lens astrological profile</h1>
      <p style={{paddingBottom: 10}}>
        Connect your wallet that holds the Lens profile to mint your 
        Soulbound natal chart NFT and retrieve your astro profile.
      </p>
      {!active && <Button text="Connect Wallet" onClick={() => setShowModal(true)}/>}
      <Modal
        title="Connect Wallet"
        buttons={[
          <Button onClick={connectBrowserWallet} text="Browser Wallet" src={ethereum_icon}  />,
          <Button text="WalletConnect" src={wallet_connect_icon} />
        ]}
        onClose={() => setShowModal(false) }
        show={showModal}
      />
      {
        (active && window.ethereum.networkVersion == POLYGON_CHAIN_ID)
        && <Button onClick={() => props.changePage("form")} text="Continue" />
      }
      {
        (active && window.ethereum.networkVersion != POLYGON_CHAIN_ID)
        && <Button onClick={() => switch2Polygon(library)} text="Switch Network" />
      }
      <p style={{paddingTop: 18}}>
        Don’t have a Lens profile?
        &nbsp;
        <a href="https://www.lens.xyz/" style={{color: 'red', fontWeight: 400}}>See how to get it.</a>
      </p>
    </div>
  )
}
