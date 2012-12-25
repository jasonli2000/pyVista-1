__author__ = 'Joe'

from VistaException import VistaException
from VistaUtils import VistaUtils
from random import randint

class RpcParameter(object):

    LITERAL = 1
    REFERENCE = 2
    LIST = 3
    WORDPROC = 4
    ENCRYPTED = 10
    MAX_INDEX = 19
    COUNT_WIDTH = 3

    TYPES = [LITERAL, REFERENCE, LIST, WORDPROC, ENCRYPTED]

    def __cipher_pad(self):
        return [
            "wkEo-ZJt!dG)49K{nX1BS$vH<&:Myf*>Ae0jQW=;|#PsO`'%+rmb[gpqN,l6/hFC@DcUa ]z~R}\"V\\iIxu?872.(TYL5_3",
            "rKv`R;M/9BqAF%&tSs#Vh)dO1DZP> *fX'u[.4lY=-mg_ci802N7LTG<]!CWo:3?{+,5Q}(@jaExn$~p\\IyHwzU\"|k6Jeb",
            "\\pV(ZJk\"WQmCn!Y,y@1d+~8s?[lNMxgHEt=uw|X:qSLjAI*}6zoF{T3#;ca)/h5%`P4$r]G'9e2if_>UDKb7<v0&- RBO.",
            "depjt3g4W)qD0V~NJar\\B \"?OYhcu[<Ms%Z`RIL_6:]AX-zG.#}$@vk7/5x&*m;(yb2Fn+l'PwUof1K{9,|EQi>H=CT8S!",
            "NZW:1}K$byP;jk)7'`x90B|cq@iSsEnu,(l-hf.&Y_?J#R]+voQXU8mrV[!p4tg~OMez CAaGFD6H53%L/dT2<*>\"{\\wI=",
            "vCiJ<oZ9|phXVNn)m K`t/SI%]A5qOWe\\&?;jT~M!fz1l>[D_0xR32c*4.P\"G{r7}E8wUgyudF+6-:B=$(sY,LkbHa#'@Q",
            "hvMX,'4Ty;[a8/{6l~F_V\"}qLI\\!@x(D7bRmUH]W15J%N0BYPkrs&9:$)Zj>u|zwQ=ieC-oGA.#?tfdcO3gp`S+En K2*<",
            "jd!W5[];4'<C$/&x|rZ(k{>?ghBzIFN}fAK\"#`p_TqtD*1E37XGVs@0nmSe+Y6Qyo-aUu%i8c=H2vJ\\) R:MLb.9,wlO~P",
            "2ThtjEM+!=xXb)7,ZV{*ci3\"8@_l-HS69L>]\\AUF/Q%:qD?1~m(yvO0e'<#o$p4dnIzKP|`NrkaGg.ufCRB[; sJYwW}5&",
            "vB\\5/zl-9y:Pj|=(R'7QJI *&CTX\"p0]_3.idcuOefVU#omwNZ`$Fs?L+1Sk<,b)hM4A6[Y%aDrg@~KqEW8t>H};n!2xG{",
            "sFz0Bo@_HfnK>LR}qWXV+D6`Y28=4Cm~G/7-5A\\b9!a#rP.l&M$hc3ijQk;),TvUd<[:I\"u1'NZSOw]*gxtE{eJp|y (?%",
            "M@,D}|LJyGO8`$*ZqH .j>c~h<d=fimszv[#-53F!+a;NC'6T91IV?(0x&/{B)w\"]Q\\YUWprk4:ol%g2nE7teRKbAPuS_X",
            ".mjY#_0*H<B=Q+FML6]s;r2:e8R}[ic&KA 1w{)vV5d,$u\"~xD/Pg?IyfthO@CzWp%!`N4Z'3-(o|J9XUE7k\\TlqSb>anG",
            "xVa1']_GU<X`|\\NgM?LS9{\"jT%s$}y[nvtlefB2RKJW~(/cIDCPow4,>#zm+:5b@06O3Ap8=*7ZFY!H-uEQk; .q)i&rhd",
            "I]Jz7AG@QX.\"%3Lq>METUo{Pp_ |a6<0dYVSv8:b)~W9NK`(r'4fs&wim\\kReC2hg=HOj$1B*/nxt,;c#y+![?lFuZ-5D}",
            "Rr(Ge6F Hx>q$m&C%M~Tn,:\"o'tX/*yP.{lZ!YkiVhuw_<KE5a[;}W0gjsz3]@7cI2\\QN?f#4p|vb1OUBD9)=-LJA+d`S8",
            "I~k>y|m};d)-7DZ\"Fe/Y<B:xwojR,Vh]O0Sc[`$sg8GXE!1&Qrzp._W%TNK(=J 3i*2abuHA4C'?Mv\\Pq{n#56LftUl@9+",
            "~A*>9 WidFN,1KsmwQ)GJM{I4:C%}#Ep(?HB/r;t.&U8o|l['Lg\"2hRDyZ5`nbf]qjc0!zS-TkYO<_=76a\\X@$Pe3+xVvu",
            "yYgjf\"5VdHc#uA,W1i+v'6|@pr{n;DJ!8(btPGaQM.LT3oe?NB/&9>Z`-}02*%x<7lsqz4OS ~E$\\R]KI[:UwC_=h)kXmF",
            "5:iar.{YU7mBZR@-K|2 \"+~`M%8sq4JhPo<_X\\Sg3WC;Tuxz,fvEQ1p9=w}FAI&j/keD0c?)LN6OHV]lGy'$*>nd[(tb!#"
        ]

    def __init__(self, type, value, encryption_indexes=None):
        if type not in self.TYPES:
            raise VistaException("Invalid param type")
        self.type = self.LITERAL if type == self.ENCRYPTED else type
        if type != self.ENCRYPTED:
            self.value = value
        elif encryption_indexes is None:
            self.value = self.encrypt(value)
        else:
            self.value = self.encrypt(value, encryption_indexes)

    def encrypt(self, value, encryption_indexes=None):
        if encryption_indexes is None:
            indexes = self.get_random_indexes()
        else:
            indexes = self.validate_indexes(encryption_indexes)
        associator_index = indexes[0]
        identifier_index = indexes[1]
        encrypted_value = ""
        for ch in value:
            pos = self.__cipher_pad()[associator_index].find(ch)
            encrypted_value += ch if pos == -1 else self.__cipher_pad()[identifier_index][pos]
        return chr(associator_index + 32) + encrypted_value + chr(identifier_index + 32)

    def get_random_indexes(self):
        associator_index = randint(0, self.MAX_INDEX)
        identifier_index = randint(0, self.MAX_INDEX)
        while associator_index == identifier_index:
            identifier_index = randint(0, self.MAX_INDEX)
        return [associator_index, identifier_index]

    def validate_indexes(self, encryption_indexes):
        if encryption_indexes[0] == encryption_indexes[1]:
            raise VistaException("Encryption indexes cannot be equal")
        for index in encryption_indexes:
            if index < 0 or index > self.MAX_INDEX:
                raise VistaException("Encryption indexes must be 0..19")
        return encryption_indexes

    @staticmethod
    def list_to_string(param_list):
        if not len(param_list):
            return VistaUtils.str_pack('', RpcParameter.COUNT_WIDTH) + 'f'

        param_string = ""
        for param in param_list:
            if param[1] == "":
                param[1] = "\x01"
            param_string += VistaUtils.str_pack(param[0], RpcParameter.COUNT_WIDTH) + \
                            VistaUtils.str_pack(param[1], RpcParameter.COUNT_WIDTH) + 't'
        return param_string[0:-1] + 'f'

    @staticmethod
    def decrypt(s):
        associator_index = ord(s[0]) - 32
        identifier_index = ord(s[-1]) - 32
        s = s[1:-1]
        decrypted_string = ""

        # This instantiation is here because Python doesn't have private constants!
        param = RpcParameter(1,"0")

        for ch in s:
            pos = param.__cipher_pad()[identifier_index].find(ch)
            decrypted_string += param.__cipher_pad()[associator_index][pos]
        return decrypted_string
