import React, { useState, useEffect, useRef } from 'react'
import Image from 'next/image';
import styles from '@/styles/Home.module.css'
import {useWindowWidth} from '@react-hook/window-size'

const Header = () => {
  /* We use a different logo in the header when viewport is small */
  const [isMobile, setIsMobile] = useState(false);

  // see: https://blog.sethcorker.com/question/how-to-solve-referenceerror-next-js-window-is-not-defined/
  useEffect(() => {
    setIsMobile(window.innerWidth <= 599 ? true : false);
  }, []);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 599 ? true : false);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <header className={styles.header}>
      <div className={styles["header-logo"]}>
        {isMobile? (
          <Image
            src="/logo.svg"
            width={200}
            height={30}
          />
        ) : (
          <Image
            src="/astrace_text.svg"
            width={200}
            height={30}
          />
        )}
      </div>
    </header>
  )
}

export default Header
