import React, { useState, useEffect } from "react";
//import {ethers} from 'ethers';
import { InjectedConnector } from '@web3-react/injected-connector';
import { useRouter } from 'next/router';
import { useWeb3React } from '@web3-react/core';
import Head from 'next/head';
import Image from 'next/image';
import Header from '../components/Header/Header.js';
import Button from '../components/Buttons/Button.js';
import Modal from '../components/Modal/Modal.js';
import Footer from '../components/Footer/Footer.js';
import styles from '@/styles/Home.module.css';
// logos
import background from '../../public/background-image.png';
import ethereum_icon from '../icons/ethereum.svg';
import wallet_connect_icon from '../icons/wallet_connect.svg';

export default function Index(props) {
  const [showModal, setShowModal] = useState(false);

  const { active, account, library, connector, activate, deactivate } = useWeb3React();

  const injected = new InjectedConnector({
    supportedChainIds: [1, 3, 4, 5, 42, 137],
  })

  async function connectBrowserWallet() {
    try {
      await activate(injected);
      localStorage.setItem('isBrowserWalletConnected', true);
      setShowModal(false);
    } catch (ex) {
      console.log(ex);
    }
  }

  async function disconnect() {
    try {
      deactivate()
      localStorage.setItem('isBrowserWalletConnected', false)
    } catch (ex) {
      console.log(ex)
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
    console.log("HERE222");
    console.log(window.ethereum.networkVersion);
  }, [])

  function isConnectedPolygon () {

  }

  return (
    <>
      <Head>
        <title>Launch LENS astrological profile</title>
        <meta name="description" content="Launch your Lens astrological profile" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className={styles.bgWrap}>
        <Image
          alt="background"
          src={background}
          placeholder="blur"
          quality={100}
          fill
          sizes="100vw"
          style={{
            objectFit: 'cover',
          }}
        />
      </div>
      <main className={styles.main}>
        <Header showWallet={false} />
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
          {(active && window.ethereum.networkVersion == 137) && <Button text="Continue" />}
          {(active && window.ethereum.networkVersion != 137) && <Button text="Switch Network" />}
          <p style={{paddingTop: 18}}>
            Don’t have a Lens profile?
            &nbsp;
            <a href="https://www.lens.xyz/" style={{color: 'red', fontWeight: 400}}>See how to get it.</a>
          </p>
          <div style={{color: "white"}}>
            <span>Active: {active.toString()}</span>
            <span>Account: {account}</span>
            <span>Active: {active}</span>
          </div>
        </div>
          <Footer/>
      </main>
    </>
  )
};
