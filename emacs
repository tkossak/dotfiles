;; Packages
(setq package-archives '(("gnu" . "http://elpa.gnu.org/packages/")
                         ("org" . "http://orgmode.org/elpa/")
                         ("marmalade" . "http://marmalade-repo.org/packages/")
                         ("melpa-stable" . "http://melpa-stable.milkbox.net/packages/")))
(package-initialize)

(if (file-accessible-directory-p "~/.emacs.d/mine")
    (add-to-list 'load-path "~/.emacs.d/mine")
  )

(if (file-accessible-directory-p "~/.emacs.d/org-mode/lisp")
    (add-to-list 'load-path "~/.emacs.d/org-mode/lisp")
  )

;; ====================================================================
;; org mode
(require 'org)
(define-key global-map "\C-cl" 'org-store-link)
(define-key global-map "\C-ca" 'org-agenda)
(define-key global-map "\C-cc" 'org-capture)

(setq org-log-done t)
(setq org-agenda-skip-deadline-prewarning-if-scheduled t)
(setq org-agenda-restore-windows-after-quit t)
(setq org-deadline-warning-days 7)
(setq org-goto-auto-isearch nil) ; additional keys for C-c C-j
;;(setq org-log-redeadline 'time) ; log changes to deadlines
;;(setq org-log-reschedule 'time) ; log changes to schedules

                                        ; Targets include this file and any file contributing to the agenda - up to 9 levels deep
(setq org-refile-targets (quote ((nil :maxlevel . 9)
                                 (org-agenda-files :maxlevel . 9))))
(setq org-archive-reversed-order t)
(setq org-archive-location "archive/archive_%s::") ; archive location
;; Use full outline paths for refile targets - we file directly with IDO
(setq org-refile-use-outline-path t)
;; Targets complete directly with IDO
(setq org-outline-path-complete-in-steps t)

                                        ; treat _ as part of the word (for example to use in "ciw")
(modify-syntax-entry ?_ "w")

(load-library ".emacs.local")


                                        ; (setq org-default-notes-file (concat org-base-path "capture_notes.org.gpg")) ;; capture file

;; add capture file to agenda files:
                                        ; (setcdr org-agenda-files (cons org-default-notes-file (cdr org-agenda-files)))
                                        ; (setcdr org-agenda-files (cons org-default-notes-file (cdr org-agenda-files)))


;; clocking
(setq org-src-fontify-natively t) ;; syntax highlighting in begin_src
(setq org-clock-into-drawer 3) ;; group clock entries into the LOGBOOK drawer
(setq org-clock-mode-line-total 'today)
(setq org-clock-report-include-clocking-task "t")

(setq org-agenda-clock-consistency-checks
      (quote
       (:max-duration "10:00" :min-duration "00:01" :max-gap "0:00" :gap-ok-around
                      ("00:00")
                      :default-face
                      ((:background "DarkRed")
                       (:foreground "white"))
                      :overlap-face nil :gap-face nil :no-end-time-face nil :long-face nil :short-face nil))
      )

; clocksums display hours, not days:
(setq org-time-clocksum-format
      '(:hours "%d" :require-hours t :minutes ":%02d" :require-minutes t))

                                        ; ======================================================================
;; for EasyPG
(if (file-readable-p "C:/cygwin64/bin/gpg.exe")
    (setq epg-gpg-program "C:/cygwin64/bin/gpg.exe")
  (if (file-readable-p "C:/cygwin/bin/gpg.exe")
      (setq epg-gpg-program "C:/cygwin/bin/gpg.exe")
    (if (file-readable-p "/usr/bin/gpg")
        (setq epg-gpg-program "/usr/bin/gpg")
      )
    )
  )
(setq epa-file-cache-passphrase-for-symmetric-encryption "true")

;; Do not use gpg agent when runing in terminal
(defadvice epg--start (around advice-epg-disable-agent activate)
  (let ((agent (getenv "GPG_AGENT_INFO")))
    (setenv "GPG_AGENT_INFO" nil)
    ad-do-it
    (setenv "GPG_AGENT_INFO" agent)))

;; (require 'package)
;; (push '("marmalade" . "http://marmalade-repo.org/packages/")
;; package-archives )
;; (push '("melpa" . "http://melpa.milkbox.net/packages/")
;; package-archives)

;; ====================================================================
;; EVIL MODE
;; ====================================================================

;; Evil-Leader

;; enable evil mode
(add-to-list 'load-path "~/.emacs.d/evil/lib")
(add-to-list 'load-path "~/.emacs.d/evil")
(setq evil-want-C-i-jump nil)

(require 'evil)
(require 'evil-leader)

(global-evil-leader-mode)
(evil-leader/set-leader "<SPC>")
(evil-leader/set-key
  "w" 'save-buffer
  "W" 'save-some-buffers
  "e" 'kill-buffer
  "E" 'save-buffers-kill-terminal)

(evil-mode 1)

;; Remap org-mode meta keys for convenience
(mapcar (lambda (state)
          (evil-declare-key state org-mode-map
            (kbd "M-l") 'org-metaright
            (kbd "M-h") 'org-metaleft
            (kbd "M-k") 'org-metaup
            (kbd "M-j") 'org-metadown
            (kbd "M-L") 'org-shiftmetaright
;;            (kbd "M-H") 'org-shiftmetaleft ; changed to org-mark-element later
            (kbd "M-K") 'org-shiftmetaup
            (kbd "M-J") 'org-shiftmetadown))
        '(normal insert))

;; for evil mode:
(define-key evil-normal-state-map (kbd "M-H") 'org-mark-element)
(define-key evil-insert-state-map (kbd "C-e") nil)
(define-key evil-insert-state-map (kbd "C-d") nil)
(define-key evil-insert-state-map (kbd "C-k") nil)
;;(define-key evil-insert-state-map (kbd "C-y") nil)
;;(define-key evil-visual-state-map (kbd "C-y") nil)
;;(define-key evil-normal-state-map (kbd "C-y") nil)
(define-key evil-insert-state-map (kbd "C-g") 'evil-normal-state)
(define-key evil-motion-state-map (kbd "C-e") nil)
;; (define-key evil-visual-state-map (kbd "C-c") 'evil-normal-state)
;; (define-key evil-visual-state-map (kbd "C-c") 'evil-exit-visual-state)
(define-key evil-visual-state-map (kbd "C-c") nil)
(define-key evil-normal-state-map (kbd "C-w q") 'delete-window)

;; (define-key evil-normal-state-map "\C-n" 'evil-next-line)
;; (define-key evil-insert-state-map "\C-n" 'evil-next-line)
;; (define-key evil-visual-state-map "\C-n" 'evil-next-line)
;; (define-key evil-normal-state-map "\C-p" 'evil-previous-line)
;; (define-key evil-insert-state-map "\C-p" 'evil-previous-line)
;; (define-key evil-visual-state-map "\C-p" 'evil-previous-line)
(define-key evil-normal-state-map "j" 'evil-next-visual-line)
(define-key evil-normal-state-map "k" 'evil-previous-visual-line)
(define-key evil-normal-state-map "gj" 'evil-next-line)
(define-key evil-normal-state-map "gk" 'evil-previous-line)
(define-key evil-visual-state-map "j" 'evil-next-visual-line)
(define-key evil-visual-state-map "k" 'evil-previous-visual-line)
(define-key evil-visual-state-map "gj" 'evil-next-line)
(define-key evil-visual-state-map "gk" 'evil-previous-line)
;; (define-key evil-normal-state-map "\C-y" 'yank)
;; (define-key evil-insert-state-map "\C-y" 'yank)
;; (define-key evil-visual-state-map "\C-y" 'yank)
(define-key evil-normal-state-map "Q" 'call-last-kbd-macro)

(define-key evil-normal-state-map (kbd "C-h") 'evil-window-left)
(define-key evil-normal-state-map (kbd "C-l") 'evil-window-right)
;(define-key evil-normal-state-map (kbd "C-j") 'evil-window-down)
;(define-key evil-normal-state-map (kbd "C-k") 'evil-window-up)
(define-key evil-normal-state-map (kbd "C-j") 'outline-next-visible-heading)
(define-key evil-normal-state-map (kbd "C-k") 'outline-previous-visible-heading)
(define-key evil-normal-state-map (kbd "C-S-k") 'outline-up-heading)


(require 'key-chord)
(setq key-chord-two-keys-delay 0.5)
(key-chord-define evil-insert-state-map "jk" 'evil-normal-state)
(key-chord-mode 1)

(define-key evil-normal-state-map ";" 'evil-ex)
(define-key evil-visual-state-map ";" 'evil-ex)
(define-key evil-normal-state-map ":" 'evil-repeat-find-char)

(setq evil-move-cursor-back nil) ;; do not move cursor left when exiting insert mode

;; evil - cursor colors depending on mode
(setq evil-emacs-state-cursor '("red" box))
(setq evil-normal-state-cursor '("green" box))
(setq evil-visual-state-cursor '("orange" box))
(setq evil-insert-state-cursor '("red" bar))
(setq evil-replace-state-cursor '("red" bar))
(setq evil-operator-state-cursor '("red" hollow))


;; esc quits
(defun minibuffer-keyboard-quit ()
  "Abort recursive edit.
In Delete Selection mode, if the mark is active, just deactivate it;
then it takes a second \\[keyboard-quit] to abort the minibuffer."
  (interactive)
  (if (and delete-selection-mode transient-mark-mode mark-active)
      (setq deactivate-mark t)
    (when (get-buffer "*Completions*") (delete-windows-on "*Completions*"))
    (abort-recursive-edit)))
(define-key evil-normal-state-map [escape] 'keyboard-quit)
(define-key evil-visual-state-map [escape] 'keyboard-quit)
(define-key minibuffer-local-map [escape] 'minibuffer-keyboard-quit)
(define-key minibuffer-local-ns-map [escape] 'minibuffer-keyboard-quit)
(define-key minibuffer-local-completion-map [escape] 'minibuffer-keyboard-quit)
(define-key minibuffer-local-must-match-map [escape] 'minibuffer-keyboard-quit)
(define-key minibuffer-local-isearch-map [escape] 'minibuffer-keyboard-quit)
(global-set-key [escape] 'evil-exit-emacs-state)

(defun hscroll-cursor-left ()
  (interactive "@")
  (set-window-hscroll (selected-window) (current-column)))

(defun hscroll-cursor-right ()
  (interactive "@")
  (set-window-hscroll (selected-window) (- (current-column) (window-width) -1)))

(define-key evil-normal-state-map "zs" 'hscroll-cursor-left)
(define-key evil-normal-state-map "ze" 'hscroll-cursor-right)
(setq auto-hscroll-mode 't)
(setq hscroll-margin 0
      hscroll-step 1)

;; ====================================================================
;; Recent Files
(require 'recentf)
(recentf-mode 1)
(setq recentf-max-menu-items 25)
(global-set-key "\C-x\ \C-r" 'recentf-open-files)

;; Rozne
(setq calendar-week-start-day 1) ;; week starts on monday
(delete-selection-mode 1) ;; pasting overwrites visual selection
(setq scroll-step 1) ;; keyboard scroll one line at a time
(setq-default tab-width 4 indent-tabs-mode nil) ;; adds spaces when TAB
(show-paren-mode t) ;; show matching parentesis
(setq make-backup-files nil) ;; do not make backups
;;(global-linum-mode t) ;; add line numbers

(setq calendar-latitude 50.3)
(setq calendar-longitude 19.1)
(setq calendar-time-zone 60)
(setq calendar-standard-time-zone-name "CET")
(setq calendar-daylight-time-zone-name "CEST")
(if (file-readable-p "~/Dropbox/Private/mydocs/org/diary")
    (setq diary-file "~/Dropbox/Private/mydocs/org/diary")
  )
(setq diary-number-of-entries 7)

(define-key global-map (kbd "RET") 'newline-and-indent) ;; add indent when RET
(define-key global-map (kbd "<f5>") 'occur) ;; search
(define-key global-map (kbd "<f4>") 'align-regexp) ;; wyrownanie do regexpa
(define-key global-map (kbd "<f2>") 'toggle-truncate-lines) ;; wyrownanie do regexpa
(define-key global-map (kbd "<f3>") 'auto-fill-mode) ;; wyrownanie do regexpa


;; do not use x clipboard:
(setq x-select-enable-clipboard nil)

(defun paste-from-clipboard ()
  (interactive)
  (setq x-select-enable-clipboard t)
  (yank)
  (setq x-select-enable-clipboard nil))

(defun copy-to-clipboard()
  (interactive)
  (setq x-select-enable-clipboard t)
  (kill-ring-save (region-beginning) (region-end))
  (setq x-select-enable-clipboard nil))

(define-key evil-normal-state-map (kbd "C-y") 'paste-from-clipboard)
(define-key evil-visual-state-map (kbd "C-y") 'copy-to-clipboard)

(evil-leader/set-key
  "y" 'copy-to-clipboard
  "p" 'paste-from-clipboard)
