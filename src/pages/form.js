import React, { useState, useEffect, Component } from "react";
import { useRouter } from 'next/router';
import {ethers} from 'ethers'
import Head from 'next/head';
import Image from 'next/image';
import Header from '../components/Header/Header.js';
import Button from '../components/Button/Button.js';
import Modal from '../components/Modal/Modal.js';
import Footer from '../components/Footer/Footer.js';
import styles from '@/styles/Home.module.css';
// logos
import background from '../../public/background-image.png';
import ethereum_icon from '../icons/ethereum.svg';
import wallet_connect_icon from '../icons/wallet_connect.svg';

function FormWithRouter(props) {
  const router = useRouter()
  return <Form {...props} router={router} />
}

class Form extends React.Component {

  constructor(props) {
    super(props);
    
    this.state = {
      showModal: false,
      defaultAccount: props.router.query["account"],
      userBalance: null,
    }
  };

  componentDidMount() {
    this.connectWalletHandler();
  }

  componentDidUpdate() {
    this.connectWalletHandler();
  }

	connectWalletHandler = () => {
		if (window.ethereum && window.ethereum.isMetaMask) {
			console.log('MetaMask Here!');

			window.ethereum.request({ method: 'eth_requestAccounts'})
			.then(result => {
				this.accountChangedHandler(result[0]);
				this.getAccountBalance(result[0]);
			})
			.catch(error => {
			  console.log("ERROR MSG");
			  console.log(error.message);
			});
      window.location.href = "/form";
		} else {
			console.log('Need to install MetaMask');
		}
	}

  // update account, will cause component re-render
	accountChangedHandler = (newAccount) => {
	  this.setState({defaultAccount: newAccount});
		this.getAccountBalance(newAccount.toString());
	}

	getAccountBalance = (account) => {
		window.ethereum.request({method: 'eth_getBalance', params: [account, 'latest']})
		.then(balance => {
		  console.log(balance);
	    this.setState({userBalance: balance});
		})
		.catch(error => {
		  console.log("ERRROR");
		  console.log(error.message);
		});
	};

	chainChangedHandler = () => {
		// reload the page to avoid any errors with chain change mid use of application
		window.location.reload();
	};


  componentDidMount() {
	  // listen for account changes
	  window.ethereum.on('accountsChanged', this.accountChangedHandler);
	  window.ethereum.on('chainChanged', this.chainChangedHandler);
  }


  render() { return (
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
        <Header walletAddress={this.state.defaultAccount} />
        <div className={styles["main-text"]}>
        </div>
          <Footer/>
      </main>
    </>
  )};
}
export default FormWithRouter;
