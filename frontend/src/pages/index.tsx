import React, { useState,  useCallback, useEffect } from "react";
import { useWeb3React } from '@web3-react/core';
import { InjectedConnector } from '@web3-react/injected-connector';
import WalletConnection from '../enums/WalletConnection';
import Head from 'next/head';
import Background from '../components/Background/Background.js';
import Header from '../components/Header/Header.js';
import Home from '../components/Home/Home.js';
import Form from '../components/Form/Form';
import Footer from '../components/Footer/Footer.js';
import styles from '../styles/Index.module.css';

const POLYGON_CHAIN_ID = 137;

/*
 * TODO: Use Template Literal Types instead of enums to keep track of page and connection.
 *
 *
 */

export default function Index(props) {
  //const { activate, deactivate, active, error, account, library } = useWeb3React();
  const { activate, active, library } = useWeb3React();
  // TODO: change to enum
  const [page, setPage] = useState("home");
  const [connStatus, setConnStatus] = useState<WalletConnection>(WalletConnection.NotConnected);
  
  const injected = new InjectedConnector({
    // we "support" all of the main ones,
    // but prompt "Switch Network" if they
    // are not Polygon
    supportedChainIds: [
      137, //Polygon
      1, 2, 3, 4, 42, 56, 42161, 43114, 10, 250, 100,
    ],
  })
  
  async function handleConnect() {
    try {
      await activate(injected);
      // let { provider } = await connector.activate();
      // web3 = new Web3(provider); 
      localStorage.setItem('isBrowserWalletConnected', 'true');
    } catch (ex) {
      console.log(ex);
    }
  }
  
  // connect on page load if already connected previously
  useEffect(() => {
    const connectWalletOnPageLoad = async () => {
      if (localStorage?.getItem('isBrowserWalletConnected') == 'true') {
        try {
          await handleConnect();
        } catch (ex) {
          console.log(ex)
        }
      }
    }
    connectWalletOnPageLoad()
  }, [])

  // if we disconnect while on this page, save that info
  useEffect(() => {
    if (!active) {
      localStorage.setItem('isBrowserWalletConnected', 'false');
    }
  }, [active])

  const wrapperSetPage = useCallback(page => {
    setPage(page);
  }, [setPage]);

  return (
    <>
      <Head>
        <title>Astrace X Lens</title>
        <meta name="description" content="Launch your Lens astrological profile" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Background />
      <div className={styles.container}>
        <Header
          page={page}
          connect={handleConnect}
        />
        <div className={styles.content}>
          {page === "home" ? (
            <Home
              changePage={wrapperSetPage}
              connect={handleConnect}
            />
          ) : (
            <Form changePage={wrapperSetPage} />
          )}
        </div>
        <Footer/>
      </div>
    </>
  )
};
