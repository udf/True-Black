import random
import colorsys
from collections import Counter, defaultdict


def to_signed_32bit(n):
    n = n & 0xffffffff
    return (n ^ 0x80000000) - 0x80000000


def hex_to_tuple(hex_str):
    # Strip leading #
    if hex_str[0] == '#':
        hex_str = hex_str[1:]

    if len(hex_str) == 6:
        hex_str = f'FF{hex_str}'

    if len(hex_str) != 8:
        raise TypeError(f'Expected hex length of 6 or 8 but got {len(hex_str)}')

    a, r, g, b = (int(hex_str[i:i + 2], 16) for i in range(0, 8, 2))

    return (r, g, b, a)


def sorted_items(dict, key=None, reverse=False):
    if key is None:
        key = lambda k, v: v
    keys = sorted(dict, key=lambda k: key(k, dict[k]), reverse=reverse)
    for k in keys:
        yield k, dict[k]


class rgba:
    colour_usage_counter = Counter()
    colour_instances = defaultdict(set)
    never_used = set()

    def __init__(self, r, g=None, b=None, a=None):
        # convert hex to tuple
        if isinstance(r, str):
            r, g, b, a = hex_to_tuple(r)

        # figure out alpha from type
        if a is None:
            a = 1.0 if isinstance(r, float) else 255

        types = tuple(type(v) for v in (r, g, b, a))
        if not all(t == types[0] for t in types):
            raise TypeError(
                f'(r, g, b) should all be of the same type but got {types}'
            )

        if not isinstance(r, (int, float)):
            raise TypeError(f'Expected ints or floats but got {type(r)}')

        # convert float (0-1) to int (0-255)
        if isinstance(r, float):
            r, g, b, a = (round(c * 255) for c in (r, g, b, a))

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        rgba.never_used.add(self)

    def as_argbhex(s):
        return ''.join(f'{c:02X}' for c in (s.a, s.r, s.g, s.b))

    def as_rgbahex(s):
        return ''.join(f'{c:02X}' for c in (s.r, s.g, s.b, s.a))

    def as_tuple(s):
        return (s.r, s.g, s.b, s.a)

    def dist(s, o):
        v = (s.r - o.r)**2
        v += (s.g - o.g)**2
        v += (s.b - o.b)**2
        v += (s.a - o.a)**2
        return v ** 0.5

    def __hash__(s):
        return hash(s.as_tuple())

    def __eq__(s, o):
        return s.as_tuple() == o.as_tuple()

    def __repr__(s):
        return f'rgba({s.r}, {s.g}, {s.b}, {s.a})'

    def __str__(s):
        rgba.colour_usage_counter.update((s,))
        rgba.colour_instances[s].add(id(s))
        rgba.never_used.discard(s)
        int_val = int(s.as_argbhex(), 16)
        return f'{to_signed_32bit(int_val)}'

    @staticmethod
    def print_warnings():
        num_warnings = 0
        for colour in rgba.never_used:
            num_warnings += 1
            print(f'Warning: {repr(colour)} is never used!')

        for colour, count in sorted_items(rgba.colour_usage_counter):
            if count >= 3:
                continue
            num_warnings += 1
            print(f'Warning: {repr(colour)} is only used {count} time(s)!')

        for colour, ids in sorted_items(rgba.colour_instances, key=lambda k, v: len(v)):
            if len(ids) <= 1:
                continue
            num_warnings += 1
            print(f'Warning: {repr(colour)} is defined by {len(ids)} instances!')

        print(f'{num_warnings} warning(s)')


class placeholder:
    def __str__(self):
        h = random.uniform(0, 1)
        s = random.uniform(0.3, 1)
        v = random.uniform(0.3, 1)
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return str(rgba(*rgb))


transparent = rgba(0, 0, 0, 0)
black = rgba(0, 0, 0)
black_10 = rgba(26, 26, 26)
black_20 = rgba(51, 51, 51)
black_30 = rgba(76, 76, 76)
black_40 = rgba(102, 102, 102)
gray = rgba(128, 128, 128)
white_60 = rgba(153, 153, 153)
white_70 = rgba(178, 178, 178)
white_80 = rgba(204, 204, 204)
white_90 = rgba(230, 230, 230)
white = rgba(255, 255, 255)

placeholder_red = rgba(255, 0, 0)
placeholder_green = rgba(0, 255, 0)
placeholder_cyan = rgba(0, 255, 255)
placeholder_yellow = rgba(255, 255, 0)

data = f'''
actionBarActionModeDefault={black}
actionBarActionModeDefaultIcon={white_90}
actionBarActionModeDefaultSelector={black_20}
actionBarActionModeDefaultTop={black_10}
actionBarDefault={black}
actionBarDefaultIcon={white}
actionBarDefaultSearch={white}
actionBarDefaultSearchPlaceholder={rgba(255, 255, 255, 128)}
actionBarDefaultSelector={black_40}
actionBarDefaultSubmenuBackground={black_20}
actionBarDefaultSubmenuItem={white_90}
actionBarDefaultSubtitle={white_60}
actionBarDefaultTitle={white}
actionBarWhiteSelector={rgba(0, 0, 0, 47)}
avatar_actionBarIconBlue={white}
avatar_actionBarIconCyan={white}
avatar_actionBarIconGreen={white}
avatar_actionBarIconOrange={white}
avatar_actionBarIconPink={white}
avatar_actionBarIconRed={white}
avatar_actionBarIconViolet={white}
avatar_actionBarSelectorBlue={black}
avatar_actionBarSelectorCyan={white_60}
avatar_actionBarSelectorGreen={white_60}
avatar_actionBarSelectorOrange={white_60}
avatar_actionBarSelectorPink={white_60}
avatar_actionBarSelectorRed={white_60}
avatar_actionBarSelectorViolet={white_60}
avatar_backgroundActionBarBlue={black_10}
avatar_backgroundActionBarCyan={black_10}
avatar_backgroundActionBarGreen={black_10}
avatar_backgroundActionBarOrange={black_10}
avatar_backgroundActionBarPink={black_10}
avatar_backgroundActionBarRed={black_10}
avatar_backgroundActionBarViolet={black_10}
avatar_backgroundArchived={black_30}
avatar_backgroundArchivedHidden={black_10}
avatar_backgroundBlue={rgba(86, 163, 219)}
avatar_backgroundCyan={rgba(95, 190, 213)}
avatar_backgroundGreen={rgba(118, 200, 77)}
avatar_backgroundGroupCreateSpanBlue={black}
avatar_backgroundInProfileBlue={black}
avatar_backgroundInProfileCyan={rgba(81, 154, 186)}
avatar_backgroundInProfileGreen={rgba(103, 179, 93)}
avatar_backgroundInProfileOrange={rgba(246, 157, 97)}
avatar_backgroundInProfilePink={rgba(243, 127, 166)}
avatar_backgroundInProfileRed={rgba(216, 111, 101)}
avatar_backgroundInProfileViolet={rgba(140, 121, 210)}
avatar_backgroundOrange={rgba(242, 140, 72)}
avatar_backgroundPink={rgba(242, 116, 154)}
avatar_backgroundRed={rgba(229, 101, 85)}
avatar_backgroundSaved={rgba(102, 191, 250)}
avatar_backgroundViolet={rgba(142, 133, 238)}
avatar_nameInMessageBlue={rgba(78, 146, 204)}
avatar_nameInMessageCyan={rgba(66, 177, 168)}
avatar_nameInMessageGreen={rgba(103, 179, 93)}
avatar_nameInMessageOrange={rgba(220, 136, 89)}
avatar_nameInMessagePink={rgba(78, 146, 204)}
avatar_nameInMessageRed={rgba(205, 90, 90)}
avatar_nameInMessageViolet={rgba(78, 146, 204)}
avatar_subtitleInProfileBlue={white_80}
avatar_subtitleInProfileCyan={white_80}
avatar_subtitleInProfileGreen={white_80}
avatar_subtitleInProfileOrange={white_80}
avatar_subtitleInProfilePink={white_80}
avatar_subtitleInProfileRed={white_80}
avatar_subtitleInProfileViolet={white_80}
avatar_text={white_90}
calls_callReceivedGreenIcon={rgba(0, 200, 83)}
calls_callReceivedRedIcon={rgba(255, 72, 72)}
calls_ratingStar={rgba(0, 0, 0, 128)}
calls_ratingStarSelected={rgba(78, 146, 204)}
changephoneinfo_image={white_70}
chat_addContact={rgba(86, 163, 219)}
chat_adminSelectedText={white}
chat_adminText={white_60}
chat_attachAudioBackground={rgba(242, 140, 72)}
chat_attachAudioIcon={white}
chat_attachCameraIcon1={rgba(255, 125, 48)}
chat_attachCameraIcon2={rgba(235, 88, 80)}
chat_attachCameraIcon3={rgba(55, 169, 240)}
chat_attachCameraIcon4={rgba(180, 85, 224)}
chat_attachCameraIcon5={rgba(97, 208, 97)}
chat_attachCameraIcon6={rgba(254, 193, 37)}
chat_attachContactIcon={white}
chat_attachFileIcon={white}
chat_attachGalleryIcon={white}
chat_attachHideBackground={white_70}
chat_attachHideIcon={white}
chat_attachLocationIcon={white}
chat_attachSendBackground={rgba(62, 193, 249)}
chat_attachSendIcon={white}
chat_attachVideoBackground={rgba(227, 113, 121)}
chat_attachVideoIcon={white}
chat_botButtonText={white}
chat_botKeyboardButtonBackground={black_10}
chat_botKeyboardButtonBackgroundPressed={black_20}
chat_botKeyboardButtonText={white}
chat_botProgress={white}
chat_botSwitchToInlineText={rgba(58, 140, 207)}
chat_editDoneIcon={rgba(81, 189, 243)}
chat_emojiPanelBackground={black}
chat_emojiPanelBackspace={black_40}
chat_emojiPanelBadgeBackground={rgba(77, 166, 234)}
chat_emojiPanelBadgeText={white}
chat_emojiPanelEmptyText={black_40}
chat_emojiPanelIcon={black_40}
chat_emojiPanelIconSelected={white}
chat_emojiPanelIconSelector={white}
chat_emojiPanelMasksIcon={white}
chat_emojiPanelMasksIconSelected={rgba(98, 191, 232)}
chat_emojiPanelNewTrending={rgba(77, 166, 234)}
chat_emojiPanelShadowLine={black_30}
chat_emojiPanelStickerPackSelector={black_10}
chat_emojiPanelStickerSetName={white_60}
chat_emojiPanelStickerSetNameIcon={white_70}
chat_emojiPanelTrendingDescription={black_40}
chat_emojiPanelTrendingTitle={white_60}
chat_fieldOverlayText={rgba(58, 140, 207)}
chat_gifSaveHintBackground={rgba(17, 17, 17, 204)}
chat_gifSaveHintText={white}
chat_goDownButton={black_30}
chat_goDownButtonCounter={white}
chat_goDownButtonCounterBackground={rgba(77, 166, 234)}
chat_goDownButtonIcon={white_80}
chat_goDownButtonShadow={black}
chat_inAudioCacheSeekbar={gray}
chat_inAudioDurationSelectedText={white_60}
chat_inAudioDurationText={white_60}
chat_inAudioPerfomerSelectedText={white_60}
chat_inAudioPerfomerText={white_60}
chat_inAudioProgress={black_20}
chat_inAudioSeekbar={black_10}
chat_inAudioSeekbarFill={rgba(114, 181, 232)}
chat_inAudioSeekbarSelected={black_40}
chat_inAudioSelectedProgress={black_20}
chat_inAudioTitleText={white_80}
chat_inBubble={black_10}
chat_inBubbleSelected={black_20}
chat_inBubbleShadow={transparent}
chat_inContactBackground={rgba(114, 181, 232)}
chat_inContactIcon={black_20}
chat_inContactNameText={rgba(81, 154, 186)}
chat_inContactPhoneSelectedText={black_20}
chat_inContactPhoneText={white_60}
chat_inFileBackground={white_60}
chat_inFileBackgroundSelected={white_60}
chat_inFileIcon={black_20}
chat_inFileInfoSelectedText={white_60}
chat_inFileInfoText={white_60}
chat_inFileNameText={white_80}
chat_inFileProgress={white_60}
chat_inFileProgressSelected={white_60}
chat_inFileSelectedIcon={black_20}
chat_inForwardedNameText={rgba(81, 154, 186)}
chat_inInstant={rgba(58, 140, 207)}
chat_inInstantSelected={rgba(48, 121, 181)}
chat_inlineResultIcon={rgba(78, 146, 204)}
chat_inLoader={black_20}
chat_inLoaderPhoto={black_20}
chat_inLoaderPhotoIcon={white_60}
chat_inLoaderPhotoIconSelected={white_80}
chat_inLoaderPhotoSelected={black_40}
chat_inLoaderSelected={black_40}
chat_inLocationBackground={white_80}
chat_inLocationIcon={black_20}
chat_inMediaIcon={white_80}
chat_inMediaIconSelected={white}
chat_inMenu={white_60}
chat_inMenuSelected={white_60}
chat_inPreviewInstantSelectedText={rgba(81, 154, 186)}
chat_inPreviewInstantText={rgba(81, 154, 186)}
chat_inPreviewLine={rgba(81, 154, 186)}
chat_inReplyLine={rgba(81, 154, 186)}
chat_inReplyMediaMessageSelectedText={white_60}
chat_inReplyMediaMessageText={white_60}
chat_inReplyMessageText={white_60}
chat_inReplyNameText={rgba(81, 154, 186)}
chat_inSentClock={white_80}
chat_inSentClockSelected={white_80}
chat_inSiteNameText={rgba(81, 154, 186)}
chat_inTimeSelectedText={white_60}
chat_inTimeText={white_60}
chat_inVenueInfoSelectedText={white_60}
chat_inVenueInfoText={rgba(93, 111, 128)}
chat_inViaBotNameText={rgba(91, 175, 211)}
chat_inViews={white_60}
chat_inViewsSelected={white_60}
chat_inVoiceSeekbar={black_10}
chat_inVoiceSeekbarFill={rgba(114, 181, 232)}
chat_inVoiceSeekbarSelected={rgba(191, 223, 246)}
chat_linkSelectBackground={rgba(98, 169, 227, 51)}
chat_lockIcon={white}
chat_mediaBroadcast={white}
chat_mediaInfoText={white}
chat_mediaLoaderPhoto={rgba(0, 0, 0, 102)}
chat_mediaLoaderPhotoIcon={white}
chat_mediaLoaderPhotoIconSelected={white_80}
chat_mediaLoaderPhotoSelected={rgba(0, 0, 0, 128)}
chat_mediaMenu={black}
chat_mediaProgress={white}
chat_mediaSentCheck={white}
chat_mediaSentClock={white}
chat_mediaTimeBackground={rgba(0, 0, 0, 102)}
chat_mediaTimeText={white}
chat_mediaViews={white}
chat_messageLinkIn={rgba(86, 163, 219)}
chat_messageLinkOut={rgba(86, 163, 219)}
chat_messagePanelBackground={black}
chat_messagePanelCancelInlineBot={white_70}
chat_messagePanelHint={rgba(153, 153, 153, 201)}
chat_messagePanelIcons={black_40}
chat_messagePanelSend={rgba(98, 176, 235)}
chat_messagePanelShadow={black}
chat_messagePanelText={white}
chat_messagePanelVoiceBackground={rgba(78, 146, 204)}
chat_messagePanelVoiceDelete={black_40}
chat_messagePanelVoiceDuration={white}
chat_messagePanelVoicePressed={white}
chat_messagePanelVoiceShadow={transparent}
chat_messageTextIn={white}
chat_messageTextOut={white}
chat_muteIcon={white_80}
chat_outAudioCacheSeekbar={gray}
chat_outAudioDurationSelectedText={white_60}
chat_outAudioDurationText={white_60}
chat_outAudioPerfomerSelectedText={white_60}
chat_outAudioPerfomerText={white_60}
chat_outAudioProgress={black_20}
chat_outAudioSeekbar={black_30}
chat_outAudioSeekbarFill={gray}
chat_outAudioSeekbarSelected={gray}
chat_outAudioSelectedProgress={black_20}
chat_outAudioTitleText={white_80}
chat_outBroadcast={rgba(70, 170, 54)}
chat_outBubble={black_10}
chat_outBubbleSelected={black_20}
chat_outBubbleShadow={transparent}
chat_outContactBackground={white_80}
chat_outContactIcon={black_20}
chat_outContactNameText={rgba(81, 154, 186)}
chat_outContactPhoneText={white_80}
chat_outFileBackground={white_60}
chat_outFileBackgroundSelected={white_60}
chat_outFileIcon={black_20}
chat_outFileInfoSelectedText={white_60}
chat_outFileInfoText={white_60}
chat_outFileNameText={white_80}
chat_outFileProgress={white_60}
chat_outFileProgressSelected={white_60}
chat_outFileSelectedIcon={black_20}
chat_outForwardedNameText={rgba(81, 154, 186)}
chat_outInstant={rgba(81, 154, 186)}
chat_outInstantSelected={rgba(81, 154, 186)}
chat_outLoader={black_20}
chat_outLoaderPhoto={black_20}
chat_outLoaderPhotoIcon={white_60}
chat_outLoaderPhotoIconSelected={white_80}
chat_outLoaderPhotoSelected={black_40}
chat_outLoaderSelected={black_40}
chat_outLocationBackground={white_80}
chat_outLocationIcon={black_20}
chat_outMediaIcon={white_80}
chat_outMediaIconSelected={white}
chat_outMenu={white_60}
chat_outMenuSelected={white_60}
chat_outPreviewInstantSelectedText={rgba(81, 154, 186)}
chat_outPreviewInstantText={rgba(81, 154, 186)}
chat_outPreviewLine={rgba(81, 154, 186)}
chat_outReplyLine={rgba(81, 154, 186)}
chat_outReplyMediaMessageSelectedText={white_60}
chat_outReplyMediaMessageText={white_60}
chat_outReplyMessageText={white_60}
chat_outReplyNameText={rgba(81, 154, 186)}
chat_outSentCheck={white}
chat_outSentCheckRead={white}
chat_outSentCheckReadSelected={white}
chat_outSentCheckSelected={white}
chat_outSentClock={white_80}
chat_outSentClockSelected={white_80}
chat_outSiteNameText={rgba(81, 154, 186)}
chat_outTimeSelectedText={white_60}
chat_outTimeText={white_60}
chat_outVenueInfoSelectedText={white_60}
chat_outVenueInfoText={white_60}
chat_outVenueNameText={white_80}
chat_outViaBotNameText={rgba(58, 140, 207)}
chat_outViews={white_60}
chat_outViewsSelected={white_60}
chat_outVoiceSeekbar={black_30}
chat_outVoiceSeekbarFill={gray}
chat_outVoiceSeekbarSelected={gray}
chat_previewDurationText={white}
chat_previewGameText={white}
chat_recordedVoiceBackground={rgba(86, 163, 219)}
chat_recordedVoiceDot={rgba(218, 86, 77)}
chat_recordedVoicePlayPause={white}
chat_recordedVoicePlayPausePressed={rgba(217, 234, 251)}
chat_recordedVoiceProgress={rgba(162, 206, 248)}
chat_recordedVoiceProgressInner={white}
chat_recordTime={black_30}
chat_recordVoiceCancel={white_60}
chat_replyPanelClose={white_70}
chat_replyPanelIcons={rgba(77, 166, 234)}
chat_replyPanelLine={transparent}
chat_replyPanelMessage={white_80}
chat_replyPanelName={rgba(58, 140, 207)}
chat_reportSpam={rgba(229, 101, 85)}
chat_searchPanelIcons={rgba(86, 163, 219)}
chat_searchPanelText={rgba(78, 146, 204)}
chat_secretChatStatusText={black_40}
chat_secretTimerBackground={rgba(0, 0, 0, 182)}
chat_secretTimerText={white}
chat_secretTimeText={white_80}
chat_selectedBackground={rgba(53, 53, 53, 102)}
chat_sentError={rgba(219, 53, 53)}
chat_sentErrorIcon={white}
chat_serviceBackground={black_10}
chat_serviceBackgroundSelected={black_20}
chat_serviceIcon={white}
chat_serviceLink={white}
chat_serviceText={white}
chat_stickerNameText={white}
chat_stickerReplyLine={white}
chat_stickerReplyMessageText={white}
chat_stickerReplyNameText={white}
chat_stickersHintPanel={black_10}
chat_stickerViaBotNameText={white}
chat_textSelectBackground={rgba(98, 169, 227, 102)}
chat_topPanelBackground={black}
chat_topPanelClose={black_30}
chat_topPanelLine={rgba(81, 154, 186)}
chat_topPanelMessage={white_80}
chat_topPanelTitle={rgba(81, 154, 186)}
chat_unreadMessagesStartArrowIcon={black_20}
chat_unreadMessagesStartBackground={white_60}
chat_unreadMessagesStartText={black_20}
chat_wallpaper={black}
chats_actionBackground={black_20}
chats_actionIcon={white}
chats_actionMessage={rgba(81, 154, 186)}
chats_actionPressedBackground={rgba(81, 154, 186)}
chats_archiveBackground={black_30}
chats_archivePinBackground={black_30}
chats_archivePullDownBackground={black_10}
chats_attachMessage={rgba(81, 154, 186)}
chats_date={black_40}
chats_draft={rgba(221, 75, 57)}
chats_mentionIcon={white}
chats_menuBackground={black}
chats_menuCloud={white}
chats_menuCloudBackgroundCats={white_60}
chats_menuItemCheck={rgba(81, 154, 186)}
chats_menuItemIcon={white_70}
chats_menuItemText={white_70}
chats_menuName={white}
chats_menuPhone={white_80}
chats_menuPhoneCats={white_80}
chats_menuTopBackgroundCats={black_10}
chats_menuTopShadow={black}
chats_message={white_60}
chats_muteIcon={black_30}
chats_name={white_80}
chats_nameArchived={white_80}
chats_nameIcon={white}
chats_nameMessage_threeLines={white_80}
chats_nameMessage={rgba(81, 154, 186)}
chats_nameMessageArchived={white_60}
chats_onlineCircle={rgba(77, 166, 234, 255)}
chats_pinnedIcon={black_40}
chats_pinnedOverlay={black}
chats_secretIcon={rgba(113, 215, 86)}
chats_secretName={rgba(113, 215, 86)}
chats_sentCheck={white}
chats_sentClock={white_60}
chats_sentError={rgba(218, 86, 77)}
chats_sentErrorIcon={white}
chats_sentReadCheck={white}
chats_tabletSelectedOverlay={black_20}
chats_unreadCounter={rgba(0, 98, 163)}
chats_unreadCounterMuted={black_20}
chats_unreadCounterText={white}
chats_verifiedBackground={rgba(55, 169, 240)}
chats_verifiedCheck={white}
checkbox={black}
checkboxCheck={white}
checkboxSquareBackground={rgba(77, 166, 234)}
checkboxSquareCheck={white}
checkboxSquareDisabled={white_70}
checkboxSquareUnchecked={black_40}
contacts_inviteBackground={rgba(85, 190, 97)}
contacts_inviteText={white}
contextProgressInner1={rgba(191, 223, 246)}
contextProgressInner2={rgba(191, 223, 246)}
contextProgressInner3={white_70}
contextProgressOuter1={rgba(25, 167, 232)}
contextProgressOuter2={white}
contextProgressOuter3={white}
dialog_liveLocationProgress={rgba(55, 169, 240)}
dialogBackground={black}
dialogBackgroundGray={black}
dialogBadgeBackground={rgba(62, 193, 249)}
dialogBadgeText={white}
dialogButton={rgba(78, 146, 204)}
dialogButtonSelector={rgba(255, 255, 255, 20)}
dialogCameraIcon={white}
dialogCheckboxSquareBackground={rgba(77, 166, 234)}
dialogCheckboxSquareCheck={white}
dialogCheckboxSquareDisabled={white_70}
dialogCheckboxSquareUnchecked={black_40}
dialogGrayLine={white_80}
dialogIcon={gray}
dialogInputField={white_80}
dialogInputFieldActivated={rgba(55, 169, 240)}
dialogLineProgress={rgba(82, 125, 163)}
dialogLineProgressBackground={white_80}
dialogLinkSelection={rgba(98, 169, 227, 51)}
dialogProgressCircle={rgba(82, 125, 163)}
dialogRadioBackground={white_70}
dialogRadioBackgroundChecked={rgba(55, 169, 240)}
dialogRoundCheckBox={rgba(62, 193, 249)}
dialogRoundCheckBoxCheck={white}
dialogScrollGlow={white_90}
dialogTextBlack={white_90}
dialogTextBlue={rgba(52, 139, 193)}
dialogTextBlue2={rgba(58, 140, 207)}
dialogTextBlue3={rgba(62, 193, 249)}
dialogTextBlue4={rgba(25, 167, 232)}
dialogTextGray={rgba(52, 139, 193)}
dialogTextGray2={black_40}
dialogTextGray3={white_60}
dialogTextGray4={white_70}
dialogTextHint={white_60}
dialogTextLink={rgba(58, 140, 207)}
dialogTextRed={rgba(205, 90, 90)}
dialogTopBackground={rgba(114, 181, 232)}
divider={transparent}
emptyListPlaceholder={black_30}
fastScrollActive={rgba(86, 163, 219)}
fastScrollInactive={black_40}
fastScrollText={white}
featuredStickers_addButton={rgba(77, 166, 234)}
featuredStickers_addButtonPressed={rgba(77, 166, 234)}
featuredStickers_addedIcon={rgba(77, 166, 234)}
featuredStickers_buttonProgress={white}
featuredStickers_buttonText={white}
featuredStickers_delButton={rgba(218, 86, 77)}
featuredStickers_delButtonPressed={rgba(198, 73, 73)}
featuredStickers_unread={rgba(77, 166, 234)}
files_folderIcon={white_70}
files_folderIconBackground={black}
files_iconText={white}
graySection={black}
groupcreate_checkbox={black}
groupcreate_checkboxCheck={white}
groupcreate_cursor={rgba(86, 163, 219)}
groupcreate_hintText={white_70}
groupcreate_offlineText={gray}
groupcreate_onlineText={rgba(58, 140, 207)}
groupcreate_sectionShadow={black}
groupcreate_sectionText={gray}
groupcreate_spanBackground={black}
groupcreate_spanText={white_90}
inappPlayerBackground={black}
inappPlayerClose={black_30}
inappPlayerPerformer={white_80}
inappPlayerPlayPause={rgba(98, 176, 235)}
inappPlayerTitle={white_80}
key_chat_messagePanelVoiceLock={white_70}
key_chat_messagePanelVoiceLockBackground={white}
key_chat_messagePanelVoiceLockShadow={black}
key_chats_menuTopShadow={transparent}
key_graySectionText={white_80}
key_sheet_scrollUp={white}
listSelector={rgba(255, 255, 255, 128)}
listSelectorSDK21={rgba(255, 255, 255, 128)}
location_liveLocationProgress={rgba(55, 169, 240)}
location_markerX={gray}
location_placeLocationBackground={rgba(77, 166, 234)}
location_sendLiveLocationBackground={rgba(255, 100, 100)}
location_sendLocationBackground={rgba(109, 160, 212)}
location_sendLocationIcon={white}
login_progressInner={rgba(217, 234, 251)}
login_progressOuter={rgba(109, 160, 212)}
musicPicker_buttonBackground={rgba(98, 176, 235)}
musicPicker_buttonIcon={white}
musicPicker_checkbox={rgba(41, 182, 247)}
musicPicker_checkboxCheck={white}
passport_authorizeBackground={rgba(77, 166, 234)}
passport_authorizeBackgroundSelected={rgba(58, 140, 207)}
passport_authorizeText={white}
picker_badge={rgba(41, 182, 247)}
picker_badgeText={white}
picker_disabledButton={white_60}
picker_enabledButton={rgba(25, 167, 232)}
player_actionBar={black_10}
player_actionBarItems={white}
player_actionBarSelector={black_10}
player_actionBarSubtitle={black_40}
player_actionBarTitle={white_90}
player_actionBarTop={black_10}
player_background={black}
player_button={gray}
player_buttonActive={rgba(41, 182, 247)}
player_placeholder={black_20}
player_placeholderBackground={white_90}
player_progress={rgba(41, 182, 247)}
player_progressBackground={rgba(0, 0, 0, 128)}
player_time={gray}
profile_actionBackground={black_20}
profile_actionIcon={white_80}
profile_actionPressedBackground={black}
profile_adminIcon={gray}
profile_creatorIcon={rgba(78, 146, 204)}
profile_status={white}
profile_title={white}
profile_verifiedBackground={rgba(178, 214, 248)}
profile_verifiedCheck={white}
progressCircle={white_80}
radioBackground={white_70}
radioBackgroundChecked={rgba(55, 169, 240)}
returnToCallBackground={rgba(77, 166, 234)}
returnToCallText={white}
sessions_devicesImage={white_60}
sharedMedia_linkPlaceholder={white_90}
sharedMedia_linkPlaceholderText={white}
sharedMedia_startStopLoadIcon={rgba(55, 169, 240)}
stickers_menu={black_30}
stickers_menuSelector={rgba(0, 0, 0, 47)}
switch2Check={white}
switch2Thumb={rgba(205, 90, 90)}
switch2ThumbChecked={rgba(77, 166, 234)}
switch2Track={rgba(255, 176, 173)}
switch2TrackChecked={rgba(162, 206, 248)}
switchThumb={white_70}
switchThumbChecked={white_90}
switchTrack={black_40}
switchTrackChecked={white_80}
undo_background={black_10}
windowBackgroundGray={black}
windowBackgroundGrayShadow={black}
windowBackgroundWhite={black}
windowBackgroundWhiteBlackText={white_80}
windowBackgroundWhiteBlueHeader={white}
windowBackgroundWhiteBlueText={rgba(81, 154, 186)}
windowBackgroundWhiteBlueText2={rgba(52, 139, 193)}
windowBackgroundWhiteBlueText3={rgba(48, 121, 181)}
windowBackgroundWhiteBlueText4={rgba(78, 146, 204)}
windowBackgroundWhiteBlueText5={rgba(78, 146, 204)}
windowBackgroundWhiteBlueText6={rgba(58, 140, 207)}
windowBackgroundWhiteBlueText7={rgba(48, 121, 181)}
windowBackgroundWhiteGrayIcon={gray}
windowBackgroundWhiteGrayLine={white_80}
windowBackgroundWhiteGrayText={black_40}
windowBackgroundWhiteGrayText2={black_40}
windowBackgroundWhiteGrayText3={black_40}
windowBackgroundWhiteGrayText4={black_40}
windowBackgroundWhiteGrayText5={white_70}
windowBackgroundWhiteGrayText6={black_40}
windowBackgroundWhiteGrayText7={white_80}
windowBackgroundWhiteGrayText8={black_40}
windowBackgroundWhiteGreenText={rgba(38, 151, 44)}
windowBackgroundWhiteGreenText2={rgba(66, 195, 102)}
windowBackgroundWhiteHintText={white_60}
windowBackgroundWhiteInputField={white_80}
windowBackgroundWhiteInputFieldActivated={rgba(55, 169, 240)}
windowBackgroundWhiteLinkSelection={rgba(98, 169, 227, 51)}
windowBackgroundWhiteLinkText={rgba(81, 154, 186)}
windowBackgroundWhiteRedText={rgba(205, 90, 90)}
windowBackgroundWhiteRedText2={rgba(218, 86, 77)}
windowBackgroundWhiteRedText3={rgba(198, 73, 73)}
windowBackgroundWhiteRedText4={rgba(219, 53, 53)}
windowBackgroundWhiteRedText5={rgba(255, 72, 72)}
windowBackgroundWhiteRedText6={rgba(255, 100, 100)}
windowBackgroundWhiteValueText={rgba(81, 154, 186)}
'''.strip()

with open('true_black.attheme', 'w') as f:
    f.write(data)

rgba.print_warnings()