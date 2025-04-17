import licenta
import ast
import extractData

# print(licenta.getPuuid("SasEUnTicnit", "SEUTs"))
# players = licenta.getSummonersWithRank("DIAMOND", 4, licenta.rankQueue, 1, 100)
players = [
    "Z_azuW98XJsOH0KGp-vEAtM-khdEisrgam-aXPDZliu3Jry6JGA15r6uIDTn9CblIg7fh5ORmIkTWg",
    "zvoMGbXIII6J27Y0LcflZ6US7bW6WSfv9YevuLhsr3RYcUK-FXH6oAPOiRwnms4PbetoMO882Xztvw",
    "CdnYUTNGoYfWf_VrH1IrIEwO2lfRSmT_or81ZQz3vsMj0aP9XvFSeX5PgKp3n_5b9JtACfSZgbmuIw",
    "H3bUR0B-QDXEf_o4I8JSLUypgTo3A7ahXlTFr4nkDdJnQtFz32GzCrRiMOs3mFuMZWiZF16bdx42AA",
    "MEFpEPyug9mRCCqJ5HsMkp-ORIhZtIrV34NScBIL7XyBgjNCvieOeOwKGlOQkaRg8Vzoc0JUGB2Hew",
    "FZjtQBIagGpDOv1tgIrx11dCvjDGduEGj7MfbErdhw6UGfRCEQtOosdFnN5m0hu7eeYaHBSkmi-eVw",
    "LZFNhF-JfHiAZBpeWTieHOwVflkgZhpCgKwdH6GfPc3sw9ZQorRgNVdfxiwpr__HEIyqFDs-Dul3Hg",
    "RU9G7Q_Ge5OiYr-2PmEvoW2O2ZGcRw9-6saGn8AFOK9Ha8Qoyv-BNiVtp8mS4V9nJ7UcEGhaRr1-4A",
    "D_phTzVtgpRaObnz9dpdnaL48Fo3DK4Ft0GO-La6wC9DQAKCezXPSzuYo27iuJgIqzlrEunFzQy7VQ",
    "3V0bBnolEBx9GkHn9nKALnr9GleoYzeHMSkbgswZ7xRfOwyfaIAKEOWSFRNNkd9Qirwkjr8A5rBeiA",
    "ehpRd0UHrUqpryKbz7KUqehR1Wp7XSoz1S6krT2hzvCgw_6MfQScgdO4riZ-1AC-KPmKYMA6jkA8TQ",
    "eLMYHBZ-af310c-sqq3IZNg-LXMaVgSDQPwDlF6P7NY6xtU43U9ig8lbyb_0WwAoGNH1IGfDEUl2Bw",
    "yX7x8U8_k2jwkGTlO9I7g0_H1poXmZj8XiLfudvQCc4MQdB3Aof_FQ2iQpTGmQ4ANNIRgVyvxKw7Bw",
    "3yI56iVHktU5dJv0HROYEngPEPulGTrRZvWnLviZPaHoepgQucmmOe0ojDF-tWIHHdhNk6PDTOQd7w",
    "WPJjYDKiJkLOW-yXyTsMgEuILR1iRi5YEN8843N0aJN4AyQbBZYheYDW8purD_pWDSxueuTovw_QIw",
    "zTbgLjBO1qrbgmjjL-TPcxdgAKbwv6pBxugdecniEqNqh06Bg2oMKQX_Bb26kcakha9mQhG-FLRnPw",
    "Wm7EunZMeJ76-4yeEr_cTEZQ_i34_yoxRIbS-hrKmxiklf7BVdU4HgVg3FpSj5hJUNMT3jdybBTpxA",
    "YUnBaPL3JMuAIO-6mn7EVoYobKW51S6_BrtwRKdI_bbnL24fBog5gQcJmlG6TYcDdqsUrIOv7g9Z0A",
    "zp_bvf_KeJ2RusuTlg6RAzMaWrK-ey5Wrl2eqGKIL2HSE1Fw7S96bXYIeHjHCZPghDJf-QNWVlZdpQ",
    "wxdQbZ6s00LYuAizt_NoOewxBHofIK6rvXXNWGsV3j7H5v1zvTiHpRhcvcDxmqCivPPoSmmVJRxvzQ",
    "RPNXU7golcyu4K-pu5-6HiVIzZ4oKfAK4F3PVM1MzaAXuPaMZRmKoMiwy9HunQVmONxDxDlrzQfWnQ",
    "X76Pgml8zJM3u6BmTVrhGeXlHRfSfD1mt9O4X7FjHQ1H1VPdRgR-oIqFdCeromJ5hbwLOcpsIQd_QQ",
    "wYMeXbOlE4XMu8LSmecHsZy1d0sMKegByw07l29Okq_XKAcVgIKXK2W8-Ir0G5R3Q2LfmahTB1Sdjg",
    "s0H5CAouxE0vvJuMmIXy0s-JOvETjETc_ulDrC7SiyOGI2AGfKVJ_pLQ1ZKMBvREwq-dOr3vd2P5FA",
    "C9gaaxpT9tahpZ4-qaLMmMPsi78Tp4VbRVkOwFXw1xEPEgL497N9_2L0-3k6hIEyH4HheYF8blxrHQ",
    "-tSoZE7JnwBa4Cvtk6-XYvZWx_XhDYBAGbmqePWH4rNbc8Qe222G-HWQxmgFIvwVddhyZFEgfeh3Tg",
    "PR6lve02AqRdSotl6shEQ8CkzuSDr1IAT_xQnUd5UfJO3X5AjeU-A15YWZ7KkAuaAspnFErZncRKSw",
    "cylUtx8EK7NL_cA4UWPHMma6ljaW2R3D4KwmzpOjrI4gB1KsypwXbKTGHGeiRDnrGmrKRem0FH7jYw",
    "xAvvLyUZ7Y8fT3DFf5TeO_2kD5h2z5EyrF1o11NZmqYXvnmKYV385Ymqk5zIdRogFLqjONzyaTDOUg",
    "mHaLl_HfOfEcmaZjHn0mhG0gQoTHR-DM68z5SpY8x4fTapbFQDXl7kU_petaG1evTkDkD58Z9YLl6g",
    "iIwnKzu8WEGNB-WuGFbdTBhIl0B_G8fGhX6g666FZy9tIqfLe_D6e7jl29S34dgNFGK8B2AyZY17yg",
    "_-kHeg2wupY3N99mF_4WxCWtUJeXuvleve1G_48mHX3IqsFEuyJY1Co6TEx4Qc6HlCh5PKKd2BFdKw",
    "KncKoGzITMKeYv8M_PowqDO80LsFY7yuv11cw4b6_884t_P2hPAqvGW29FpullhdmtvTt5bBAH0cKw",
    "zKEttN76U2ZW-ZIhRQvMtNj5Rk90lg0ITRcmT2XJJ0REWgXSjz7y8LPOKgYtdxD2bQmLG2ADJ42aPA",
    "Gv03am8RCAVLgH5eFtArzlV7PHQvbplgU9jM9vKuVw4oJkiKKSebDmS-KO0Ipapv57n1cgL4cq6sjw",
    "_lBtq7XKymS77aSdCxISYyiwwVgMi2WxPHfTUCtPG7HrwgevqjxXtXxiRURkC5D4ANcsFvzW3Scsiw",
    "MJ1sB_7e7SbmBAiiHN9EVOowbK4H8LJ238uXN6Pgf0K-xaPWo0dFDhEfqgBGuzlNWsejTCs6D9qbPg",
    "F1CiFYN9RZXpReMj7rOnnl7yjITKwpyR4RsT7W-BFNR1JOhNwW3uLkLi5IrM8r5dzY3PY--MaBxavA",
    "o0XWppNZEluaDHd5rDCmquk52uqkh1DGvmAarGWqCw08oJ__Fr5DOfgzuYaF7rOkzemrk8dvgSNGMQ",
    "bM_47O59TJaDzwu5Jh3kHzfVyUCEz2XXrc_yPCRpprg1PnbDUi6mY-AmdMTMLH_U1lE_JCCbsk3vig",
    "91g1DlAFBFVSrCuQg8Kf5VoHcawyxh4t6jPjYbrnGouGgIT8de6JmRETmzm6psuOK3k-BWFSrnaZ7A",
    "uDwYvPb3os4sLxiivwp-8V6Xu7gcWAt3ynYvtTCvynkBCDfbc5_Q1Z1nB2xmhPoUJWyrLouIqljpTw",
    "6XsSMMEl5RrPUJ9uNqVr1Ppjik2JI0rztuTlf8OFqvjfFpmUV3H1-s4nW391tDN2mU4Him0BA-kp-w",
    "0GoWA6qMytohkqTLJyvA3bwiAeqo_8_CsZ17uOqmTGCjMbFn6sILMkUBC7Rbg7GM3PP2wISN01ykUA",
    "2texQHK9K_MDzscyJxi6lBQuwRxXjUW4mhMC3TLXEDatPEewRditRUfJhGRN_l02Z9lle9txwx1Ffg",
    "XHXKbPEogS8pq6VBkVddKV912kp3Bohd6gtO1dXc2FuwVE8Jhno9hAICRH_L4b8wc2ieFKJkrJr3mA",
    "rFqy72fBl4ku1DwXXw5dlJdHkU4c4cp18oM09uwPQ595Hwpv0Mp2RWLAY4lqmsWRu-izUKT1KstDAA",
    "kCcGwBshzFzid8VkWUPxqSZdM8XooLvt7G-33Z05r9GnyGd8H1KWojnl_m9nh6sCz5ixrRearc_h6g",
    "TbK-NM8pH0x4eQ9qbk23N9SFJHPdIILHTW1a_75VC9hHxwnePVurZ43lUSCxoqIUOsm_gOAccUOkPw",
    "NmSyBG1_JAB47hB05hPHh5-cYgAuMPvQZyHD3mnhzUD2tnELRn4Z7HSRcIKY4Qs70hyZhpMI8aMagw",
    "sijXvXo6jImu7eLfi7z6CxxZSyvKwzTb33LX3blcXGWIFk28z9TE5wog3mMtSXbNTBozDU8jcwyCSQ",
    "VnxzwHvejsB90FUeRVf51qA9hr8Rju1tyNQzWkJv4Pak9o7uc-DRVOgYJTMUDOS9CHBAtjgClMT11w",
    "4x_hRsdSUBMmU_He3KGl3JQtTbWuonWypDzqRLkfyCC76UhWEEdl_gWq1L-GAsnt0GO6s_1NRODyqw",
    "4fA1DROZvKAKuUu1C12pYxkqZjyIzX68NgVSvHIKWPeF0TtDJyu_9hCABXR1Vh3UMJM_F9-ocCa90g",
    "gagg9P2GndbeGJVl0ERb1TaldkOwCEcg1FtZhbDPtVM0deZVmlE4a3Al8qg5FGe1P_OiBD_poVTqMQ",
    "wGn63ul7DVfkhHQO5XTld6Oo4gqrKMyMe5mkiJh1mowXrDUkjOlw0fSzHHWkkcWsdMQyHcT_9zyKZw",
    "USdWNorVQnxLgE_YUpmwNoNhjGg-fImm9FNC_-il2fm8XfGn3tXg7c2jwposQQJEWyErjRsHIhJx3A",
    "MrPOpaCIOmyo7jh2Ax7hit4HAuZTaHGgy0L5tnLRM6FVARsgeEeXUkNspj1FhQdaDR8enVUHzcPYRw",
    "ivlOTII2c7NaAP8B1vcglfIbc5YVV0mXbAwf8A3YAdKE9K6MvWrXp1nnAYw5ecZvX58ABkbaFCosPg",
    "LbX6lU5TH4kit8X7TUL-TY006kiUWV_Azuf7LjM-ha41zuax4AZlMoI8J9tQM--m4Ovhd8ooinGSOQ",
    "i3w7pn8nxhoeFO0dOFOVJ9grBSAdfO_dPuKwyxuSCZ6JP2tvZ5xgISjlKPmwGfA8IMsaq5PVAaj77g",
    "RMW4Ds8jyueWaOVXtgSKW3Xu0xeh02XBRWoo9IM8pTyT7P7jMto8XrW8bQFJR84-W49b_3NP2JWAug",
    "oPNpGZJzUoVLVT7B66FVxTEURWmJj4LlNZViSmhD-d199gmhMLeo8yx-0Jr3jez6jZNPTHLgMsXXbw",
    "hcFphKk9dMT13wIPQZnenQ8VIbgkx57wXsr0yxb2vjOszCEpJXoiGTdNWc9-ySE9qxvbym6ajlUlhA",
    "oRkBXDrSCjYLB-zlU7ZNC5_5PCOnBsUs3QSnU6KxHgS0eAlWyvWt4DJ4zWdUPx-l_EyQElPxyYVd0Q",
    "34B2QlZ9svYVNlq6WyToPrl65HHCXm4XwsveDzCTWhmJ6r2bBiKK8oQf_bdRoNV0rupZSwyDoDsy8A",
    "enHsn6jEWBXl6I8Q2ARBCSlxmKSNZ0wHff_360fYoo-DlkDUFuUDEE1asnz2hhx8-slTYdtHLqclVg",
    "kFTEQdS5CA7R-StJUOGbRmCS6WpqCT3n93YSFzkRdvYZ7LU4F30s_7Sw1FDgn9qv6PslUnPQgJJglQ",
    "O5CN1e8U__O_EVdRrBXpwbvBK4v5ChHVtGg4xGT03_fgwdLMN3HJUbsUvsuKSrt4aH0GXkb09Oj-zg",
    "M1CK0tFH0aaPlpemdbU6I8L7ezEvxyg-jzv14Zexwcq0tRTfUcM9G4Xfvr3SBUg_AHyKjlREVqDKqw",
    "dedKTeDUvUmfzL4WULv2ls6581UNdSNJzQgRqBKKUmDY1y_cmBZtAYTFyFZLwpwiXTCfJ9UUAiTQ7w",
    "jBKPddUq7jZ6mzO5JfFkOj18TdceNYQS4Pjv-7VjXZnKg4wHEkdARHTm6C2X7VdzZMMz3uamgJTjDg",
    "N0adfutxLda50-pv-F-3UQjeYx84q9xLPV1o5LdRoooWwfKsVww_lxzhI8oOT-IPkRLxrIS7KdMd0A",
    "nQx_zXhb3ziyBM3rusOGF3M_XyObcVMQ30lAF2LmfUZxnEW6arTO73_ghE6UH0Uq8Z3I1p_rXINxBg",
    "yVAszT9GoAZv_Nw_t8TMrqI21zcGJ5HF6lc7RtnY1x8WSYAEnJV8i7m_wtNAYrHmY-hN21yrB4X60A",
    "Hq9XVFxMpqjzVncoUQ8ZaWedFQ7p073niv9LAlEIvRbKEzeT9_JayXK4bxK3cpMUbI9EuONmkz0sKg",
    "VMMEaR_Q3-4dp-Rp4EMlBAlgwD9iekK353-cDp4dv7q-AeAqBuWi0vze7mItIJpNYk0GGcdquOa45w",
    "w2Y8G9uRSGCkem72XXUisH4tsRGq_0qwI45pdt_evisUtHHVKsv9tVjc7l01MXQlKOa1jULGAgHi3A",
    "ZtS__ldEhu7hMjm1RdUAnMrbUGZYUeh7IL7JlEm0kx9BifvbBVM9KIlqQxesW9ceZbU85axD7p20xg",
    "cHfcoasri30fkFMp9QXnmFmvr5BHnaTTyED5VwA1iXL6Vyvhj3IE59S7yVX9CqvITT_qAjpPcYMqbA",
    "PMbCmWb57pJAko9t1A89ER5kQYFWbvbrQ_LAT0AgzdoXauZQ46UTnzWshBQSYyf2vw3sOwE3tB0hvg",
    "mj7x4xWlX4AlM-4fww8RldZm9iygWTsZewWBXIeETeiyYu-eBvjhSiD_Bzsk2BPr1g0TlXZjMPGJ-g",
    "-4rMd2xDxSk_rUCsr9JI9FQRGZyg-TebgIdTl-iiCQnpg_NnHgW-py2XZv8JyDR7TMpUC5OpoCqqWw",
    "RoRAU6MCNu9aaKNlFije-9I-bTeD9AcOoT3O6K32Ge1J2aRBNC0OGwNF6ssZb6gPfrpOvtJ_liHS0g",
    "5KHvM1IFQMG36pOOOXjSraVewmcE2zbs-dfU6BO0gLSpdDl6zdHtjRf4YDdLBzNAkIyaDGmHW2AWUQ",
    "xJ0ozIM7sj0o9vl7NK1-enyLcPuGC7XNzKgM3mdPiY2S6QTXbbr1c998DdaL-Tx0bSBexrrlwdRnWw",
    "n6S1zJhRR-VVeV8bY7eV_feIhCPK4GzssiM191Cyvd7RV7e2-xjlJYioDYvm8LY2FlYnaL9zajd2VQ",
    "N49J-GsgcAZ-tjGrzEtqQF6nByexVpoLrnnt-o8aMIbuL3wV7qCqNfPTdUjeoRAkPvzktURxwb-MNA",
    "JtuYLoZ1ZH-7yZHqfWByeHSlhKuTbokhoft553-Z7VQQDLgpbOAXQW4dKIeQNJDHjvKZ9AzilvmmYw",
    "hop2M-rbLr7MKmlWeihJjCJxcsctVn0g8OG91E96DImU1koF4Le6fXbncKqYQTFjd6-MdutuqtvwQg",
    "st2zsyabi4P4aCFXjzqJBz2zGOBeEXESEC2YrsUQ9jeE6FxaZ5onC83T9-vCshtmGYt3sV-48FfGbA",
    "crdnJcKA1Zuhbl4Sg1GBQ8PiFPw7A1HScvy7QsRhqAqDC1wPZ1U3O0cx8-vy-_PS-d8ipWJc648g_Q",
    "Szg1g54huxRcQd3H9RiyxbBUM2wVtIoA0gL0Llng3xcf8pUBnVR5Hh5ssmEVIHZKP-lKxsPy35jVNw",
    "tbydtEGE3R1wRRDDtf5vRntkiZHIp3VwLfMomF82Ki98b-a69FA_TW_kX2BSCnT-R87hBoewcEMuGw",
    "-Kmf9xBOABbY9lsVxhIoo7W7p_t7PIF7BOJIk7THZqqguAWHchci6KZLcIae1c40DIw14ZfoRBGa0w",
    "Gby3420MY8tiy4i3zgpG7_AF065qq-8r2tHPbiKIXuHm9o9k_HRjGj7lhobjd_IR-F_Evd_TKMsDRg",
    "IbJe9RqIA28jG8DOQGTGo52X5-aiXaeW6UUgPw9yIzmqJd8hpthDdE4aCxyjGXBQwEfw3JwUjxwmTQ",
    "PGITpx_fUBXowkWaU7bIj7KGqEF3gimXq7U02ekR_F8ForZ4eJHhijZmnxW7nNnblUWhWGcfKsVCOQ",
    "zB1GjV-RWsonjdf70HwZy5LQdCWAq2US4NxufyhGUsfR7_SgZB6dyho7Iz_h70E6Gg8SC04rNK1tlQ"
    ]

print(len(players))
# with open("matchIds.txt", 'a') as matchIdsFile:
#     for index in range(0, len(players)):
#         matchIds = licenta.getMatchIds(players[index], 0, 20)
#         matchIdsFile.write(str(matchIds))
#         if index != len(players) - 1:
#             matchIdsFile.write("\n")
with open("matchIds.txt", 'r') as matchIdsFile:
    l = []
    for line in matchIdsFile:
        words = ast.literal_eval(line.strip())
        l.extend(words)
    print(len(l))
    myset = set(l)
    print(len(myset))
    i = 1
    extractData.matches_to_API_to_JSON_to_CSV(myset, "output/test.json", "output/test.csv")
