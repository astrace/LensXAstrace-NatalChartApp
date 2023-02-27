import React, { useState,  useCallback } from "react";
import Head from 'next/head';
import Background from '../components/Background/Background.js';
import Header from '../components/Header/Header.js';
import Home from '../components/Home/Home.js';
import Form from '../components/Form/Form.js';
import Footer from '../components/Footer/Footer.js';
import styles from '../styles/Index.module.css';

export default function Index(props) {
  // TODO: change to enum
  const [page, setPage] = useState("home");

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
      <div className={styles.main}>
        <Header showWallet={false} page={"home"}/>
        {page == "home" && <Home changePage={wrapperSetPage} />}
        {page == "form" && <Form changePage={wrapperSetPage} />}
        <Footer/>
      </div>
    </>
  )
};
