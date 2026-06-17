# SYM Layer Draft

Converted to the Totem 38-key layout:

```dts
        sym {
            label = "SYM";
            bindings = <
              &none     &kp TILDE  &kp PRCNT  &kp ASTRK  &none     /**/  &none     &kp LBKT   &kp BSLH   &kp RBKT   &none
              &kp GRAVE &kp CARET  &kp MINUS  &kp PLUS   &kp DLLR  /**/  &kp HASH  &kp LPAR   &kp LBRC   &kp RPAR   &kp RBRC
&none         &kp PIPE  &kp AMPS   &kp LT     &kp GT     &kp DQT   /**/  &kp SQT   &kp EQUAL  &kp UNDER  &kp COLON  &kp AT    &none
                                    &trans     &trans     &trans    /**/  &trans    &trans     &trans
            >;
        };
```

## Pair Layer Draft

Mirrored by finger role. `x` from the sketch is represented as `&none`.

```text
Left visual:          Right visual:
} ) { ( x            x ( { ) }
x x ] [ x            x [ ] x x
```

```dts
        sym_pair {
            label = "SYM_PAIR";
            bindings = <
              &none     &none     &none     &none     &none     /**/  &none     &none     &none     &none     &none
              &kp RBRC  &kp RPAR  &kp LBRC  &kp LPAR  &none     /**/  &none     &kp LPAR  &kp LBRC  &kp RPAR  &kp RBRC
&none         &none     &none     &kp RBKT  &kp LBKT  &none     /**/  &none     &kp LBKT  &kp RBKT  &none     &none     &none
                                    &trans   &trans    &trans    /**/  &trans    &trans    &trans
            >;
        };
```
