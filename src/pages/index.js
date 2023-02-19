import React, { useState, useEffect } from "react";
import { useWeb3React } from '@web3-react/core';
import { InjectedConnector } from '@web3-react/injected-connector';
import { switch2Polygon} from '../utils/networkConnect.js';
import Head from 'next/head';
import Background from '../components/Background/Background.js';
import Header from '../components/Header/Header.js';
import Home from '../components/Home/Home.js';
import Button from '../components/Buttons/Button.js';
import Modal from '../components/Modal/Modal.js';
import Footer from '../components/Footer/Footer.js';
import styles from '@/styles/Home.module.css';
// logos
import ethereum_icon from '../icons/ethereum.svg';
import wallet_connect_icon from '../icons/wallet_connect.svg';

const POLYGON_CHAIN_ID = 137;

export default function Index(props) {
  const [showModal, setShowModal] = useState(false);
  
  // TODO: change to enum
  const [whichPage, setWhichPage] = useState("home");

  return (
    <>
      <Head>
        <title>Astrace X Lens</title>
        <meta name="description" content="Launch your Lens astrological profile" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Background />
      <main className={styles.main}>
        <Header showWallet={false} />
        {whichPage == "home" && <Home />}
        <Footer/>
      </main>
    </>
  )
};
