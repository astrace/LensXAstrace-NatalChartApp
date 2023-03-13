import React, { useState, useEffect } from 'react';
import { useWeb3React } from '@web3-react/core';
import { InjectedConnector } from '@web3-react/injected-connector';
import { switch2Polygon} from '../../utils/networkConnect.js';
import WalletConnection from '../../enums/WalletConnection.tsx';
import Button from '../Buttons/Button.js';
import Modal from '../Modal/Modal.js';
import styles from './Home.module.css'
// logos
import ethereum_icon from '../../icons/ethereum.svg';
import wallet_connect_icon from '../../icons/wallet_connect.svg';

export default function Home(props) {
  const [showModal, setShowModal] = useState(false);
  const { active, chainId, library } = useWeb3React();
 
  function ConnButton() {
    console.log("Connection Button function");
    console.log(active, chainId);
    if (!active) {
      // Case: Wallet is not connected
      // Display: "Connect Wallet" button & render modal when clicked 
      return (
        <>
          <Button text="Connect Wallet" onClick={() => setShowModal(true)}/>
          <Modal
            title="Connect Wallet"
            buttons={[
              <Button onClick={props.connect} text="Browser Wallet" src={ethereum_icon}  />,
              <Button text="WalletConnect" src={wallet_connect_icon} />
            ]}
            onClose={() => setShowModal(false) }
            show={showModal}
          />
        </>
      )
    } else {
      if (chainId === 137){
        // Case: Wallet is connected to Polygon
        // Display: "Continue" button & change page when clicked 
        return <Button onClick={() => props.changePage("form")} text="Continue" />
      } else {
        // Case: Wallet *is* connected, but not to Polygon
        // Display: "Switch Network" button & call `switch2Polygon` when clicked 
        return <Button onClick={switch2Polygon(library)} text="Switch Network" />
      }
    }
  }

  return (
    <div className={styles["main-text"]}>

      <h1>Launch your Lens astrological profile</h1>
      <p style={{paddingBottom: 10}}>
        Connect your wallet that holds the Lens profile to mint your 
        Soulbound natal chart NFT and retrieve your astro profile.
      </p>

      <ConnButton />
      
      <p style={{paddingTop: 18}}>
        Don’t have a Lens profile?
        &nbsp;
        <a href="https://www.lens.xyz/" style={{color: 'red', fontWeight: 400}}>See how to get it.</a>
      </p>

    </div>
  )
}
