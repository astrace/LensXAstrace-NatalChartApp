import React, { useState, Component } from "react";
//import {ethers} from 'ethers';
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

// see: https://stackoverflow.com/questions/57027469/how-to-use-userouter-from-next-js-in-a-class-component
function HomeWithRouter(props) {
  const router = useRouter()
  return <Home {...props} router={router} />
}

class Home extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      router: props.router,
      showModal: false,
      defaultAccount: null,
      userBalance: null,
    };
  };

	connectWalletHandler = () => {
		if (window.ethereum && window.ethereum.isMetaMask) {
			console.log('MetaMask Here!');

			window.ethereum.request({ method: 'eth_requestAccounts'})
			.then(result => {
				this.accountChangedHandler(result[0]);
				this.getAccountBalance(result[0]);
        this.state.router.push({
          pathname: '/form',
          query: {account: result[0]}  
        }, '/form');
			})
			.catch(error => {
			  console.log("ERROR MSG");
			  console.log(error.message);
			});
      //window.location.href = "/form";
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
        <Header showWallet={false} />
        <div className={styles["main-text"]}>
          <h1>Launch your Lens astrological profile</h1>
          <p style={{paddingBottom: 10}}>
            Connect your wallet that holds the Lens profile to mint your 
            Soulbound natal chart NFT and retrieve your astro profile.
          </p>
          <Button text="Connect Wallet" onClick={() => this.setState({ showModal: true }) }/>
          <Modal
            title="Connect Wallet"
            buttons={[
              <Button onClick={this.connectWalletHandler} text="Browser Wallet" src={ethereum_icon}  />,
              <Button text="WalletConnect" src={wallet_connect_icon} />
            ]}
            onClose={() => this.setState({ showModal: false }) }
            show={this.state.showModal}
          />
          <p style={{paddingTop: 18}}>
            Don’t have a Lens profile?
            &nbsp;
            <a href="https://www.lens.xyz/" style={{color: 'red', fontWeight: 400}}>See how to get it.</a>
          </p>
        </div>
          <Footer/>
      </main>
    </>
  )};
}

export default HomeWithRouter;
