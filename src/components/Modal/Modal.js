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
          <div className={styles["modal-content"]} onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h4 className={styles["modal-title"]}>{props.title}</h4>
            </div>
            <div className={styles["modal-body"]}>
            {props.children}
            </div>
            <div className="modal-footer">
              <button onClick={props.onClose} className="button">Close</button>
            </div>
          </div>
        </div>
      </CSSTransition>
  );
};

export default Modal;

