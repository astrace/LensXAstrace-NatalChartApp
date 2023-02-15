import React, { useEffect } from "react";
import ReactDOM from "react-dom";
import { CSSTransition } from "react-transition-group";
import styles from "./Modal.module.css";

const Modal = props => {
  return (
      <CSSTransition
        in={props.show}
        classNames="fade"
        unmountOnExit
        timeout={{ enter: 200, exit: 200 }}
      >
      <div className={styles.modal} onClick={props.onClose}>
        <div className={styles["modal-box"]} onClick={e => e.stopPropagation()}>
          <div className={styles["modal-header"]}>
            <button onClick={props.onClose} className={styles["cancel-button"]}>
            </button>
          </div>
          <div className={styles["modal-body"]}>
            <h4 className={styles["modal-title"]}>{props.title}</h4>
            {props.buttons}
          </div>
        </div>
      </div>
      </CSSTransition>
  );
};

export default Modal;

