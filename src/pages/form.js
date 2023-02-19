import React, { useState, useEffect, Component } from "react";
import { useRouter } from 'next/router';
import { useWeb3React } from '@web3-react/core';
import { InjectedConnector } from "@web3-react/injected-connector";
//import {ethers} from 'ethers'
import Head from 'next/head';
import Image from 'next/image';
import Header from '../components/Header/Header.js';
import Modal from '../components/Modal/Modal.js';
import Footer from '../components/Footer/Footer.js';
import styles from '@/styles/Form.module.css';
// logos
import background from '../../public/background-image.png';
import ethereum_icon from '../icons/ethereum.svg';
import wallet_connect_icon from '../icons/wallet_connect.svg';

export default function Form() {

  const { 
    activate,
    deactivate,
    active,
    chainId,
    account
  } = useWeb3React();
  
  //const [isConnected, setIsConnected] = useState(0);

  const Injected = new InjectedConnector({
   supportedChainIds: [1, 3, 4, 5, 42]
  });

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
        <Header showWallet={true} />
        <div className={styles.container}>
          <div className={styles.backButton}>← Go Back</div>
          <h1>Launch your Lens astrological profile </h1>
          <form>
            <div className={styles.inputContainer}>
              <input type="text" id="birthplace" name="birthplace" placeholder="Place of birth"/>
            </div>
            <div className={styles.inputContainer}>
              <input type="text" id="date" name="date" placeholder="MM / DD / YY"/>
            </div>
            <div className={styles.inputContainer}>
              <input type="text" id="time" name="time" placeholder="HH : MM"/>
            </div>
          </form>
          <div>Connection Status: {active}</div>
    <div>Account: {account}</div>
    <div>Network ID: {chainId}</div>
        </div>
        <Footer/>
      </main>
    </>
)};
