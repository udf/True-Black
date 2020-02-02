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

        for colour, count in rgba.colour_usage_counter.items():
            if count >= 3:
                continue
            num_warnings += 1
            print(f'Warning: {repr(colour)} is only used {count} time(s)!')

        for colour, ids in rgba.colour_instances.items():
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
white = rgba(255, 255, 255)
white_90 = rgba(0.9, 0.9, 0.9)
white_80 = rgba(0.8, 0.8, 0.8)
white_70 = rgba(0.7, 0.7, 0.7)
white_60 = rgba(0.6, 0.6, 0.6)

data = f'''
actionBarActionModeDefault={black}
actionBarActionModeDefaultIcon={white_90}
actionBarActionModeDefaultSelector={rgba(15, 25, 35, 122)}
actionBarActionModeDefaultTop={rgba(0, 0, 0, 164)}
actionBarDefault={black}
actionBarDefaultIcon={white}
actionBarDefaultSearch={white}
actionBarDefaultSearchPlaceholder={rgba(255, 255, 255, 128)}
actionBarDefaultSelector={rgba(99, 99, 99, 255)}
actionBarDefaultSubmenuBackground={black}
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
avatar_backgroundActionBarBlue={rgba(26, 26, 26, 255)}
avatar_backgroundActionBarCyan={rgba(26, 26, 26, 255)}
avatar_backgroundActionBarGreen={rgba(26, 26, 26, 255)}
avatar_backgroundActionBarOrange={rgba(26, 26, 26, 255)}
avatar_backgroundActionBarPink={rgba(26, 26, 26, 255)}
avatar_backgroundActionBarRed={rgba(26, 26, 26, 255)}
avatar_backgroundActionBarViolet={rgba(26, 26, 26, 255)}
avatar_backgroundArchived={rgba(77, 77, 77, 255)}
avatar_backgroundArchivedHidden={rgba(26, 26, 26, 255)}
avatar_backgroundBlue={rgba(86, 163, 219, 255)}
avatar_backgroundCyan={rgba(95, 190, 213, 255)}
avatar_backgroundGreen={rgba(118, 200, 77, 255)}
avatar_backgroundGroupCreateSpanBlue={black}
avatar_backgroundInProfileBlue={black}
avatar_backgroundInProfileCyan={rgba(81, 154, 186, 255)}
avatar_backgroundInProfileGreen={rgba(103, 179, 93, 255)}
avatar_backgroundInProfileOrange={rgba(246, 157, 97, 255)}
avatar_backgroundInProfilePink={rgba(243, 127, 166, 255)}
avatar_backgroundInProfileRed={rgba(216, 111, 101, 255)}
avatar_backgroundInProfileViolet={rgba(140, 121, 210, 255)}
avatar_backgroundOrange={rgba(242, 140, 72, 255)}
avatar_backgroundPink={rgba(242, 116, 154, 255)}
avatar_backgroundRed={rgba(229, 101, 85, 255)}
avatar_backgroundSaved={rgba(102, 191, 250, 255)}
avatar_backgroundViolet={rgba(142, 133, 238, 255)}
avatar_nameInMessageBlue={rgba(78, 146, 204, 255)}
avatar_nameInMessageCyan={rgba(66, 177, 168, 255)}
avatar_nameInMessageGreen={rgba(103, 179, 93, 255)}
avatar_nameInMessageOrange={rgba(220, 136, 89, 255)}
avatar_nameInMessagePink={rgba(78, 146, 204, 255)}
avatar_nameInMessageRed={rgba(205, 90, 90, 255)}
avatar_nameInMessageViolet={rgba(78, 146, 204, 255)}
avatar_subtitleInProfileBlue={rgba(136, 136, 136, 255)}
avatar_subtitleInProfileCyan={white_80}
avatar_subtitleInProfileGreen={white_80}
avatar_subtitleInProfileOrange={rgba(136, 136, 136, 255)}
avatar_subtitleInProfilePink={white_80}
avatar_subtitleInProfileRed={white_80}
avatar_subtitleInProfileViolet={white_80}
avatar_text={white}
calls_callReceivedGreenIcon={rgba(0, 200, 83, 255)}
calls_callReceivedRedIcon={rgba(255, 72, 72, 255)}
calls_ratingStar={rgba(0, 0, 0, 128)}
calls_ratingStarSelected={rgba(78, 146, 204, 255)}
changephoneinfo_image={rgba(168, 168, 168, 255)}
chat_addContact={rgba(86, 163, 219, 255)}
chat_adminSelectedText={white}
chat_adminText={white}
chat_attachAudioBackground={rgba(242, 140, 72, 255)}
chat_attachAudioIcon={white}
chat_attachCameraIcon1={rgba(255, 125, 48, 255)}
chat_attachCameraIcon2={rgba(235, 88, 80, 255)}
chat_attachCameraIcon3={rgba(55, 169, 240, 255)}
chat_attachCameraIcon4={rgba(180, 85, 224, 255)}
chat_attachCameraIcon5={rgba(97, 208, 97, 255)}
chat_attachCameraIcon6={rgba(254, 193, 37, 255)}
chat_attachContactIcon={white}
chat_attachFileIcon={white}
chat_attachGalleryIcon={white}
chat_attachHideBackground={white_70}
chat_attachHideIcon={white}
chat_attachLocationIcon={white}
chat_attachSendBackground={rgba(62, 193, 249, 255)}
chat_attachSendIcon={white}
chat_attachVideoBackground={rgba(227, 113, 121, 255)}
chat_attachVideoIcon={white}
chat_botButtonText={white}
chat_botKeyboardButtonBackground={rgba(26, 26, 26, 255)}
chat_botKeyboardButtonBackgroundPressed={rgba(51, 51, 51, 255)}
chat_botKeyboardButtonText={white}
chat_botProgress={white}
chat_botSwitchToInlineText={rgba(58, 140, 207, 255)}
chat_editDoneIcon={rgba(81, 189, 243, 255)}
chat_emojiPanelBackground={black}
chat_emojiPanelBackspace={rgba(115, 115, 115, 255)}
chat_emojiPanelBadgeBackground={rgba(77, 166, 234, 255)}
chat_emojiPanelBadgeText={white}
chat_emojiPanelEmptyText={rgba(99, 99, 99, 255)}
chat_emojiPanelIcon={rgba(115, 115, 115, 255)}
chat_emojiPanelIconSelected={white}
chat_emojiPanelIconSelector={white}
chat_emojiPanelMasksIcon={white}
chat_emojiPanelMasksIconSelected={rgba(98, 191, 232, 255)}
chat_emojiPanelNewTrending={rgba(77, 166, 234, 255)}
chat_emojiPanelShadowLine={rgba(77, 77, 77, 255)}
chat_emojiPanelStickerPackSelector={rgba(26, 26, 26, 255)}
chat_emojiPanelStickerSetName={white_60}
chat_emojiPanelStickerSetNameIcon={white_70}
chat_emojiPanelTrendingDescription={rgba(115, 115, 115, 255)}
chat_emojiPanelTrendingTitle={white_60}
chat_fieldOverlayText={rgba(58, 140, 207, 255)}
chat_gifSaveHintBackground={rgba(17, 17, 17, 204)}
chat_gifSaveHintText={white}
chat_goDownButton={rgba(77, 77, 77, 255)}
chat_goDownButtonCounter={white}
chat_goDownButtonCounterBackground={rgba(77, 166, 234, 255)}
chat_goDownButtonIcon={white_80}
chat_goDownButtonShadow={black}
chat_inAudioCacheSeekbar={rgba(136, 136, 136, 255)}
chat_inAudioDurationSelectedText={white_60}
chat_inAudioDurationText={white_60}
chat_inAudioPerfomerSelectedText={white_60}
chat_inAudioPerfomerText={white_60}
chat_inAudioProgress={rgba(51, 51, 51, 255)}
chat_inAudioSeekbar={rgba(26, 26, 26, 255)}
chat_inAudioSeekbarFill={rgba(114, 181, 232, 255)}
chat_inAudioSeekbarSelected={rgba(115, 115, 115, 255)}
chat_inAudioSelectedProgress={rgba(51, 51, 51, 255)}
chat_inAudioTitleText={white_80}
chat_inBubble={rgba(26, 26, 26, 255)}
chat_inBubbleSelected={rgba(51, 51, 51, 255)}
chat_inBubbleShadow={transparent}
chat_inContactBackground={rgba(114, 181, 232, 255)}
chat_inContactIcon={rgba(51, 51, 51, 255)}
chat_inContactNameText={rgba(81, 154, 186, 255)}
chat_inContactPhoneSelectedText={rgba(51, 51, 51, 255)}
chat_inContactPhoneText={white_60}
chat_inFileBackground={white_60}
chat_inFileBackgroundSelected={white_60}
chat_inFileIcon={rgba(51, 51, 51, 255)}
chat_inFileInfoSelectedText={white_60}
chat_inFileInfoText={white_60}
chat_inFileNameText={white_80}
chat_inFileProgress={white_60}
chat_inFileProgressSelected={white_60}
chat_inFileSelectedIcon={rgba(51, 51, 51, 255)}
chat_inForwardedNameText={rgba(81, 154, 186, 255)}
chat_inInstant={rgba(58, 140, 207, 255)}
chat_inInstantSelected={rgba(48, 121, 181, 255)}
chat_inlineResultIcon={rgba(78, 146, 204, 255)}
chat_inLoader={white_60}
chat_inLoaderPhoto={rgba(26, 26, 26, 255)}
chat_inLoaderPhotoIcon={white_60}
chat_inLoaderPhotoIconSelected={white_80}
chat_inLoaderPhotoSelected={rgba(51, 51, 51, 255)}
chat_inLoaderSelected={white_80}
chat_inLocationBackground={white_90}
chat_inLocationIcon={rgba(162, 181, 199, 255)}
chat_inMediaIcon={white}
chat_inMediaIconSelected={white}
chat_inMenu={white_60}
chat_inMenuSelected={white_60}
chat_inPreviewInstantSelectedText={rgba(81, 154, 186, 255)}
chat_inPreviewInstantText={rgba(81, 154, 186, 255)}
chat_inPreviewLine={rgba(81, 154, 186, 255)}
chat_inReplyLine={rgba(81, 154, 186, 255)}
chat_inReplyMediaMessageSelectedText={white_60}
chat_inReplyMediaMessageText={white_60}
chat_inReplyMessageText={white_60}
chat_inReplyNameText={rgba(81, 154, 186, 255)}
chat_inSentClock={white_80}
chat_inSentClockSelected={white_80}
chat_inSiteNameText={rgba(81, 154, 186, 255)}
chat_inTimeSelectedText={white_60}
chat_inTimeText={white_60}
chat_inVenueInfoSelectedText={white_60}
chat_inVenueInfoText={rgba(93, 111, 128, 255)}
chat_inViaBotNameText={rgba(91, 175, 211, 255)}
chat_inViews={white_60}
chat_inViewsSelected={white_60}
chat_inVoiceSeekbar={rgba(26, 26, 26, 255)}
chat_inVoiceSeekbarFill={rgba(114, 181, 232, 255)}
chat_inVoiceSeekbarSelected={rgba(191, 223, 246, 255)}
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
chat_messageLinkIn={rgba(86, 163, 219, 255)}
chat_messageLinkOut={rgba(86, 163, 219, 255)}
chat_messagePanelBackground={black}
chat_messagePanelCancelInlineBot={rgba(168, 168, 168, 255)}
chat_messagePanelHint={rgba(153, 153, 153, 201)}
chat_messagePanelIcons={rgba(99, 99, 99, 255)}
chat_messagePanelSend={rgba(98, 176, 235, 255)}
chat_messagePanelShadow={black}
chat_messagePanelText={white}
chat_messagePanelVoiceBackground={rgba(78, 146, 204, 255)}
chat_messagePanelVoiceDelete={rgba(115, 115, 115, 255)}
chat_messagePanelVoiceDuration={white}
chat_messagePanelVoicePressed={white}
chat_messagePanelVoiceShadow={transparent}
chat_messageTextIn={white}
chat_messageTextOut={white}
chat_muteIcon={white_80}
chat_outAudioCacheSeekbar={rgba(136, 136, 136, 255)}
chat_outAudioDurationSelectedText={white_60}
chat_outAudioDurationText={white_60}
chat_outAudioPerfomerSelectedText={white_60}
chat_outAudioPerfomerText={white_60}
chat_outAudioProgress={rgba(51, 51, 51, 255)}
chat_outAudioSeekbar={rgba(87, 87, 87, 255)}
chat_outAudioSeekbarFill={rgba(136, 136, 136, 255)}
chat_outAudioSeekbarSelected={rgba(136, 136, 136, 255)}
chat_outAudioSelectedProgress={rgba(51, 51, 51, 255)}
chat_outAudioTitleText={white_80}
chat_outBroadcast={rgba(70, 170, 54, 255)}
chat_outBubble={rgba(26, 26, 26, 255)}
chat_outBubbleSelected={rgba(51, 51, 51, 255)}
chat_outBubbleShadow={transparent}
chat_outContactBackground={white_80}
chat_outContactIcon={rgba(51, 51, 51, 255)}
chat_outContactNameText={rgba(81, 154, 186, 255)}
chat_outContactPhoneText={white_80}
chat_outFileBackground={white_60}
chat_outFileBackgroundSelected={white_60}
chat_outFileIcon={rgba(51, 51, 51, 255)}
chat_outFileInfoSelectedText={white_60}
chat_outFileInfoText={white_60}
chat_outFileNameText={white_80}
chat_outFileProgress={white_60}
chat_outFileProgressSelected={white_60}
chat_outFileSelectedIcon={rgba(51, 51, 51, 255)}
chat_outForwardedNameText={rgba(81, 154, 186, 255)}
chat_outInstant={rgba(81, 154, 186, 255)}
chat_outInstantSelected={rgba(81, 154, 186, 255)}
chat_outLoader={white_60}
chat_outLoaderPhoto={rgba(26, 26, 26, 255)}
chat_outLoaderPhotoIcon={white_60}
chat_outLoaderPhotoIconSelected={white_80}
chat_outLoaderPhotoSelected={rgba(51, 51, 51, 255)}
chat_outLoaderSelected={white_80}
chat_outLocationBackground={white_80}
chat_outLocationIcon={rgba(51, 51, 51, 255)}
chat_outMediaIcon={white}
chat_outMediaIconSelected={white}
chat_outMenu={white_60}
chat_outMenuSelected={white_60}
chat_outPreviewInstantSelectedText={rgba(81, 154, 186, 255)}
chat_outPreviewInstantText={rgba(81, 154, 186, 255)}
chat_outPreviewLine={rgba(81, 154, 186, 255)}
chat_outReplyLine={rgba(81, 154, 186, 255)}
chat_outReplyMediaMessageSelectedText={white_60}
chat_outReplyMediaMessageText={white_60}
chat_outReplyMessageText={white_60}
chat_outReplyNameText={rgba(81, 154, 186, 255)}
chat_outSentCheck={white}
chat_outSentCheckRead={white}
chat_outSentCheckSelected={white}
chat_outSentClock={white_80}
chat_outSentClockSelected={white_80}
chat_outSiteNameText={rgba(81, 154, 186, 255)}
chat_outTimeSelectedText={white_60}
chat_outTimeText={white_60}
chat_outVenueInfoSelectedText={white_60}
chat_outVenueInfoText={white_60}
chat_outVenueNameText={white_80}
chat_outViaBotNameText={rgba(58, 140, 207, 255)}
chat_outViews={white_60}
chat_outViewsSelected={white_60}
chat_outVoiceSeekbar={rgba(87, 87, 87, 255)}
chat_outVoiceSeekbarFill={rgba(136, 136, 136, 255)}
chat_outVoiceSeekbarSelected={rgba(136, 136, 136, 255)}
chat_previewDurationText={white}
chat_previewGameText={white}
chat_recordedVoiceBackground={rgba(86, 163, 219, 255)}
chat_recordedVoiceDot={rgba(218, 86, 77, 255)}
chat_recordedVoicePlayPause={white}
chat_recordedVoicePlayPausePressed={rgba(217, 234, 251, 255)}
chat_recordedVoiceProgress={rgba(162, 206, 248, 255)}
chat_recordedVoiceProgressInner={white}
chat_recordTime={rgba(77, 77, 77, 255)}
chat_recordVoiceCancel={white_60}
chat_replyPanelClose={rgba(168, 168, 168, 255)}
chat_replyPanelIcons={rgba(77, 166, 234, 255)}
chat_replyPanelLine={transparent}
chat_replyPanelMessage={white_80}
chat_replyPanelName={rgba(58, 140, 207, 255)}
chat_reportSpam={rgba(229, 101, 85, 255)}
chat_searchPanelIcons={rgba(86, 163, 219, 255)}
chat_searchPanelText={rgba(78, 146, 204, 255)}
chat_secretChatStatusText={rgba(99, 99, 99, 255)}
chat_secretTimerBackground={rgba(0, 0, 0, 182)}
chat_secretTimerText={white}
chat_secretTimeText={white_80}
chat_selectedBackground={rgba(53, 53, 53, 102)}
chat_sentError={rgba(219, 53, 53, 255)}
chat_sentErrorIcon={white}
chat_serviceBackground={rgba(26, 26, 26, 255)}
chat_serviceBackgroundSelected={rgba(51, 51, 51, 255)}
chat_serviceIcon={white}
chat_serviceLink={white}
chat_serviceText={white}
chat_stickerNameText={white}
chat_stickerReplyLine={white}
chat_stickerReplyMessageText={white}
chat_stickerReplyNameText={white}
chat_stickersHintPanel={rgba(26, 26, 26, 255)}
chat_stickerViaBotNameText={white}
chat_textSelectBackground={rgba(98, 169, 227, 102)}
chat_topPanelBackground={black}
chat_topPanelClose={rgba(87, 87, 87, 255)}
chat_topPanelLine={rgba(81, 154, 186, 255)}
chat_topPanelMessage={white_80}
chat_topPanelTitle={rgba(81, 154, 186, 255)}
chat_unreadMessagesStartArrowIcon={rgba(51, 51, 51, 255)}
chat_unreadMessagesStartBackground={white_60}
chat_unreadMessagesStartText={rgba(51, 51, 51, 255)}
chat_wallpaper={black}
chats_actionBackground={white_60}
chats_actionIcon={white}
chats_actionMessage={rgba(81, 154, 186, 255)}
chats_actionPressedBackground={rgba(81, 154, 186, 255)}
chats_archiveBackground={rgba(77, 77, 77, 255)}
chats_archivePinBackground={rgba(77, 77, 77, 255)}
chats_archivePullDownBackground={rgba(26, 26, 26, 255)}
chats_attachMessage={rgba(81, 154, 186, 255)}
chats_date={rgba(99, 99, 99, 255)}
chats_draft={rgba(221, 75, 57, 255)}
chats_mentionIcon={white}
chats_menuBackground={black}
chats_menuCloud={white}
chats_menuCloudBackgroundCats={white_60}
chats_menuItemCheck={rgba(81, 154, 186, 255)}
chats_menuItemIcon={rgba(168, 168, 168, 255)}
chats_menuItemText={rgba(168, 168, 168, 255)}
chats_menuName={white}
chats_menuPhone={white_80}
chats_menuPhoneCats={white_80}
chats_menuTopBackgroundCats={rgba(26, 26, 26, 255)}
chats_menuTopShadow={black}
chats_message={white_60}
chats_muteIcon={rgba(87, 87, 87, 255)}
chats_name={white_80}
chats_nameArchived={white_80}
chats_nameIcon={white}
chats_nameMessage_threeLines={white_80}
chats_nameMessage={rgba(81, 154, 186, 255)}
chats_nameMessageArchived={white_60}
chats_pinnedIcon={rgba(115, 115, 115, 255)}
chats_pinnedOverlay={black}
chats_secretIcon={rgba(113, 215, 86, 255)}
chats_secretName={rgba(113, 215, 86, 255)}
chats_sentCheck={white}
chats_sentClock={white_60}
chats_sentError={rgba(218, 86, 77, 255)}
chats_sentErrorIcon={white}
chats_sentReadCheck={white}
chats_tabletSelectedOverlay={rgba(51, 51, 51, 255)}
chats_unreadCounter={rgba(0, 98, 163, 255)}
chats_unreadCounterMuted={rgba(99, 99, 99, 255)}
chats_unreadCounterText={white}
chats_verifiedBackground={rgba(55, 169, 240, 255)}
chats_verifiedCheck={white}
checkbox={black}
checkboxCheck={white}
checkboxSquareBackground={rgba(77, 166, 234, 255)}
checkboxSquareCheck={white}
checkboxSquareDisabled={white_70}
checkboxSquareUnchecked={rgba(115, 115, 115, 255)}
contacts_inviteBackground={rgba(85, 190, 97, 255)}
contacts_inviteText={white}
contextProgressInner1={rgba(191, 223, 246, 255)}
contextProgressInner2={rgba(191, 223, 246, 255)}
contextProgressInner3={white_70}
contextProgressOuter1={rgba(25, 167, 232, 255)}
contextProgressOuter2={white}
contextProgressOuter3={white}
dialog_liveLocationProgress={rgba(55, 169, 240, 255)}
dialogBackground={black}
dialogBackgroundGray={black}
dialogBadgeBackground={rgba(62, 193, 249, 255)}
dialogBadgeText={white}
dialogButton={rgba(78, 146, 204, 255)}
dialogButtonSelector={rgba(255, 255, 255, 20)}
dialogCameraIcon={white}
dialogCheckboxSquareBackground={rgba(77, 166, 234, 255)}
dialogCheckboxSquareCheck={white}
dialogCheckboxSquareDisabled={white_70}
dialogCheckboxSquareUnchecked={rgba(115, 115, 115, 255)}
dialogGrayLine={white_80}
dialogIcon={rgba(136, 136, 136, 255)}
dialogInputField={white_80}
dialogInputFieldActivated={rgba(55, 169, 240, 255)}
dialogLineProgress={rgba(82, 125, 163, 255)}
dialogLineProgressBackground={white_80}
dialogLinkSelection={rgba(98, 169, 227, 51)}
dialogProgressCircle={rgba(82, 125, 163, 255)}
dialogRadioBackground={white_70}
dialogRadioBackgroundChecked={rgba(55, 169, 240, 255)}
dialogRoundCheckBox={rgba(62, 193, 249, 255)}
dialogRoundCheckBoxCheck={white}
dialogScrollGlow={white_90}
dialogTextBlack={white_90}
dialogTextBlue={rgba(52, 139, 193, 255)}
dialogTextBlue2={rgba(58, 140, 207, 255)}
dialogTextBlue3={rgba(62, 193, 249, 255)}
dialogTextBlue4={rgba(25, 167, 232, 255)}
dialogTextGray={rgba(52, 139, 193, 255)}
dialogTextGray2={rgba(115, 115, 115, 255)}
dialogTextGray3={white_60}
dialogTextGray4={white_70}
dialogTextHint={white_60}
dialogTextLink={rgba(58, 140, 207, 255)}
dialogTextRed={rgba(205, 90, 90, 255)}
dialogTopBackground={rgba(114, 181, 232, 255)}
divider={transparent}
emptyListPlaceholder={rgba(77, 77, 77, 255)}
fastScrollActive={rgba(86, 163, 219, 255)}
fastScrollInactive={rgba(99, 99, 99, 255)}
fastScrollText={white}
featuredStickers_addButton={rgba(77, 166, 234, 255)}
featuredStickers_addButtonPressed={rgba(77, 166, 234, 255)}
featuredStickers_addedIcon={rgba(77, 166, 234, 255)}
featuredStickers_buttonProgress={white}
featuredStickers_buttonText={white}
featuredStickers_delButton={rgba(218, 86, 77, 255)}
featuredStickers_delButtonPressed={rgba(198, 73, 73, 255)}
featuredStickers_unread={rgba(77, 166, 234, 255)}
files_folderIcon={rgba(168, 168, 168, 255)}
files_folderIconBackground={black}
files_iconText={white}
graySection={black}
groupcreate_checkbox={black}
groupcreate_checkboxCheck={white}
groupcreate_cursor={rgba(86, 163, 219, 255)}
groupcreate_hintText={rgba(168, 168, 168, 255)}
groupcreate_offlineText={rgba(136, 136, 136, 255)}
groupcreate_onlineText={rgba(58, 140, 207, 255)}
groupcreate_sectionShadow={black}
groupcreate_sectionText={rgba(136, 136, 136, 255)}
groupcreate_spanBackground={black}
groupcreate_spanText={white_90}
inappPlayerBackground={black}
inappPlayerClose={rgba(87, 87, 87, 255)}
inappPlayerPerformer={white_80}
inappPlayerPlayPause={rgba(98, 176, 235, 255)}
inappPlayerTitle={white_80}
key_chat_messagePanelVoiceLock={rgba(168, 168, 168, 255)}
key_chat_messagePanelVoiceLockBackground={white}
key_chat_messagePanelVoiceLockShadow={black}
key_chats_menuTopShadow={transparent}
key_graySectionText={white_80}
key_sheet_scrollUp={white}
listSelector={rgba(255, 255, 255, 128)}
listSelectorSDK21={rgba(255, 255, 255, 128)}
location_liveLocationProgress={rgba(55, 169, 240, 255)}
location_markerX={rgba(136, 136, 136, 255)}
location_placeLocationBackground={rgba(77, 166, 234, 255)}
location_sendLiveLocationBackground={rgba(255, 100, 100, 255)}
location_sendLocationBackground={rgba(109, 160, 212, 255)}
location_sendLocationIcon={white}
login_progressInner={rgba(217, 234, 251, 255)}
login_progressOuter={rgba(109, 160, 212, 255)}
musicPicker_buttonBackground={rgba(98, 176, 235, 255)}
musicPicker_buttonIcon={white}
musicPicker_checkbox={rgba(41, 182, 247, 255)}
musicPicker_checkboxCheck={white}
passport_authorizeBackground={rgba(77, 166, 234, 255)}
passport_authorizeBackgroundSelected={rgba(58, 140, 207, 255)}
passport_authorizeText={white}
picker_badge={rgba(41, 182, 247, 255)}
picker_badgeText={white}
picker_disabledButton={white_60}
picker_enabledButton={rgba(25, 167, 232, 255)}
player_actionBar={rgba(26, 26, 26, 255)}
player_actionBarItems={white}
player_actionBarSelector={rgba(26, 26, 26, 255)}
player_actionBarSubtitle={rgba(99, 99, 99, 255)}
player_actionBarTitle={white_90}
player_actionBarTop={rgba(26, 26, 26, 255)}
player_background={black}
player_button={rgba(136, 136, 136, 255)}
player_buttonActive={rgba(41, 182, 247, 255)}
player_placeholder={rgba(51, 51, 51, 255)}
player_placeholderBackground={white_90}
player_progress={rgba(41, 182, 247, 255)}
player_progressBackground={rgba(0, 0, 0, 128)}
player_time={rgba(136, 136, 136, 255)}
profile_actionBackground={rgba(51, 51, 51, 255)}
profile_actionIcon={white_80}
profile_actionPressedBackground={black}
profile_adminIcon={rgba(136, 136, 136, 255)}
profile_creatorIcon={rgba(78, 146, 204, 255)}
profile_status={white}
profile_title={white}
profile_verifiedBackground={rgba(178, 214, 248, 255)}
profile_verifiedCheck={white}
progressCircle={white_80}
radioBackground={white_70}
radioBackgroundChecked={rgba(55, 169, 240, 255)}
returnToCallBackground={rgba(77, 166, 234, 255)}
returnToCallText={white}
sessions_devicesImage={white_60}
sharedMedia_linkPlaceholder={white_90}
sharedMedia_linkPlaceholderText={white}
sharedMedia_startStopLoadIcon={rgba(55, 169, 240, 255)}
stickers_menu={rgba(77, 77, 77, 255)}
stickers_menuSelector={rgba(0, 0, 0, 47)}
switch2Check={white}
switch2Thumb={rgba(205, 90, 90, 255)}
switch2ThumbChecked={rgba(77, 166, 234, 255)}
switch2Track={rgba(255, 176, 173, 255)}
switch2TrackChecked={rgba(162, 206, 248, 255)}
switchThumb={rgba(168, 168, 168, 255)}
switchThumbChecked={white_90}
switchTrack={rgba(115, 115, 115, 255)}
switchTrackChecked={white_80}
undo_background={rgba(26, 26, 26, 255)}
windowBackgroundGray={rgba(26, 26, 26, 255)}
windowBackgroundGrayShadow={black}
windowBackgroundWhite={black}
windowBackgroundWhiteBlackText={white_80}
windowBackgroundWhiteBlueHeader={white}
windowBackgroundWhiteBlueText={rgba(81, 154, 186, 255)}
windowBackgroundWhiteBlueText2={rgba(52, 139, 193, 255)}
windowBackgroundWhiteBlueText3={rgba(48, 121, 181, 255)}
windowBackgroundWhiteBlueText4={rgba(78, 146, 204, 255)}
windowBackgroundWhiteBlueText5={rgba(78, 146, 204, 255)}
windowBackgroundWhiteBlueText6={rgba(58, 140, 207, 255)}
windowBackgroundWhiteBlueText7={rgba(48, 121, 181, 255)}
windowBackgroundWhiteGrayIcon={rgba(136, 136, 136, 255)}
windowBackgroundWhiteGrayLine={white_80}
windowBackgroundWhiteGrayText={rgba(99, 99, 99, 255)}
windowBackgroundWhiteGrayText2={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGrayText3={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGrayText4={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGrayText5={rgba(168, 168, 168, 255)}
windowBackgroundWhiteGrayText6={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGrayText7={white_80}
windowBackgroundWhiteGrayText8={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGreenText={rgba(38, 151, 44, 255)}
windowBackgroundWhiteGreenText2={rgba(66, 195, 102, 255)}
windowBackgroundWhiteHintText={white_60}
windowBackgroundWhiteInputField={white_80}
windowBackgroundWhiteInputFieldActivated={rgba(55, 169, 240, 255)}
windowBackgroundWhiteLinkSelection={rgba(98, 169, 227, 51)}
windowBackgroundWhiteLinkText={rgba(81, 154, 186, 255)}
windowBackgroundWhiteRedText={rgba(205, 90, 90, 255)}
windowBackgroundWhiteRedText2={rgba(218, 86, 77, 255)}
windowBackgroundWhiteRedText3={rgba(198, 73, 73, 255)}
windowBackgroundWhiteRedText4={rgba(219, 53, 53, 255)}
windowBackgroundWhiteRedText5={rgba(255, 72, 72, 255)}
windowBackgroundWhiteRedText6={rgba(255, 100, 100, 255)}
windowBackgroundWhiteValueText={rgba(81, 154, 186, 255)}
'''.strip()

with open('true_black.attheme', 'w') as f:
    f.write(data)

rgba.print_warnings()