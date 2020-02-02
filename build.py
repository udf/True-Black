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

data = f'''
actionBarActionModeDefault={black}
actionBarActionModeDefaultIcon={rgba(245, 245, 245, 255)}
actionBarActionModeDefaultSelector={rgba(15, 25, 35, 122)}
actionBarActionModeDefaultTop={rgba(0, 0, 0, 164)}
actionBarDefault={black}
actionBarDefaultIcon={white}
actionBarDefaultSearch={white}
actionBarDefaultSearchPlaceholder={rgba(255, 255, 255, 128)}
actionBarDefaultSelector={rgba(99, 99, 99, 255)}
actionBarDefaultSubmenuBackground={black}
actionBarDefaultSubmenuItem={rgba(245, 245, 245, 255)}
actionBarDefaultSubtitle={rgba(153, 153, 153, 255)}
actionBarDefaultTitle={white}
actionBarWhiteSelector={rgba(0, 0, 0, 47)}
avatar_actionBarIconBlue={white}
avatar_actionBarIconCyan={white}
avatar_actionBarIconGreen={white}
avatar_actionBarIconOrange={white}
avatar_actionBarIconPink={white}
avatar_actionBarIconRed={white}
avatar_actionBarIconViolet={white}
avatar_actionBarSelectorBlue={rgba(8, 9, 9, 255)}
avatar_actionBarSelectorCyan={rgba(153, 153, 153, 255)}
avatar_actionBarSelectorGreen={rgba(153, 153, 153, 255)}
avatar_actionBarSelectorOrange={rgba(153, 153, 153, 255)}
avatar_actionBarSelectorPink={rgba(153, 153, 153, 255)}
avatar_actionBarSelectorRed={rgba(153, 153, 153, 255)}
avatar_actionBarSelectorViolet={rgba(153, 153, 153, 255)}
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
avatar_subtitleInProfileCyan={rgba(212, 215, 214, 255)}
avatar_subtitleInProfileGreen={rgba(212, 215, 214, 255)}
avatar_subtitleInProfileOrange={rgba(136, 136, 136, 255)}
avatar_subtitleInProfilePink={rgba(212, 215, 214, 255)}
avatar_subtitleInProfileRed={rgba(212, 215, 214, 255)}
avatar_subtitleInProfileViolet={rgba(212, 215, 214, 255)}
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
chat_attachHideBackground={rgba(179, 179, 179, 255)}
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
chat_emojiPanelStickerSetName={rgba(153, 153, 153, 255)}
chat_emojiPanelStickerSetNameIcon={rgba(188, 188, 188, 255)}
chat_emojiPanelTrendingDescription={rgba(115, 115, 115, 255)}
chat_emojiPanelTrendingTitle={rgba(153, 153, 153, 255)}
chat_fieldOverlayText={rgba(58, 140, 207, 255)}
chat_gifSaveHintBackground={rgba(17, 17, 17, 204)}
chat_gifSaveHintText={white}
chat_goDownButton={rgba(77, 77, 77, 255)}
chat_goDownButtonCounter={white}
chat_goDownButtonCounterBackground={rgba(77, 166, 234, 255)}
chat_goDownButtonIcon={rgba(212, 215, 214, 255)}
chat_goDownButtonShadow={black}
chat_inAudioCacheSeekbar={rgba(136, 136, 136, 255)}
chat_inAudioDurationSelectedText={rgba(153, 153, 153, 255)}
chat_inAudioDurationText={rgba(153, 153, 153, 255)}
chat_inAudioPerfomerSelectedText={rgba(153, 153, 153, 255)}
chat_inAudioPerfomerText={rgba(153, 153, 153, 255)}
chat_inAudioProgress={rgba(51, 51, 51, 255)}
chat_inAudioSeekbar={rgba(26, 26, 26, 255)}
chat_inAudioSeekbarFill={rgba(114, 181, 232, 255)}
chat_inAudioSeekbarSelected={rgba(115, 115, 115, 255)}
chat_inAudioSelectedProgress={rgba(51, 51, 51, 255)}
chat_inAudioTitleText={rgba(212, 215, 214, 255)}
chat_inBubble={rgba(26, 26, 26, 255)}
chat_inBubbleSelected={rgba(51, 51, 51, 255)}
chat_inBubbleShadow={rgba(0, 0, 0, 0)}
chat_inContactBackground={rgba(114, 181, 232, 255)}
chat_inContactIcon={rgba(51, 51, 51, 255)}
chat_inContactNameText={rgba(81, 154, 186, 255)}
chat_inContactPhoneSelectedText={rgba(51, 51, 51, 255)}
chat_inContactPhoneText={rgba(153, 153, 153, 255)}
chat_inFileBackground={rgba(153, 153, 153, 255)}
chat_inFileBackgroundSelected={rgba(153, 153, 153, 255)}
chat_inFileIcon={rgba(51, 51, 51, 255)}
chat_inFileInfoSelectedText={rgba(153, 153, 153, 255)}
chat_inFileInfoText={rgba(153, 153, 153, 255)}
chat_inFileNameText={rgba(212, 215, 214, 255)}
chat_inFileProgress={rgba(153, 153, 153, 255)}
chat_inFileProgressSelected={rgba(153, 153, 153, 255)}
chat_inFileSelectedIcon={rgba(51, 51, 51, 255)}
chat_inForwardedNameText={rgba(81, 154, 186, 255)}
chat_inInstant={rgba(58, 140, 207, 255)}
chat_inInstantSelected={rgba(48, 121, 181, 255)}
chat_inlineResultIcon={rgba(78, 146, 204, 255)}
chat_inLoader={rgba(153, 153, 153, 255)}
chat_inLoaderPhoto={rgba(26, 26, 26, 255)}
chat_inLoaderPhotoIcon={rgba(153, 153, 153, 255)}
chat_inLoaderPhotoIconSelected={rgba(212, 215, 214, 255)}
chat_inLoaderPhotoSelected={rgba(51, 51, 51, 255)}
chat_inLoaderSelected={rgba(212, 215, 214, 255)}
chat_inLocationBackground={rgba(245, 245, 245, 255)}
chat_inLocationIcon={rgba(162, 181, 199, 255)}
chat_inMediaIcon={white}
chat_inMediaIconSelected={white}
chat_inMenu={rgba(153, 153, 153, 255)}
chat_inMenuSelected={rgba(153, 153, 153, 255)}
chat_inPreviewInstantSelectedText={rgba(81, 154, 186, 255)}
chat_inPreviewInstantText={rgba(81, 154, 186, 255)}
chat_inPreviewLine={rgba(81, 154, 186, 255)}
chat_inReplyLine={rgba(81, 154, 186, 255)}
chat_inReplyMediaMessageSelectedText={rgba(153, 153, 153, 255)}
chat_inReplyMediaMessageText={rgba(153, 153, 153, 255)}
chat_inReplyMessageText={rgba(153, 153, 153, 255)}
chat_inReplyNameText={rgba(81, 154, 186, 255)}
chat_inSentClock={rgba(197, 197, 197, 255)}
chat_inSentClockSelected={rgba(197, 197, 197, 255)}
chat_inSiteNameText={rgba(81, 154, 186, 255)}
chat_inTimeSelectedText={rgba(153, 153, 153, 255)}
chat_inTimeText={rgba(153, 153, 153, 255)}
chat_inVenueInfoSelectedText={rgba(153, 153, 153, 255)}
chat_inVenueInfoText={rgba(93, 111, 128, 255)}
chat_inViaBotNameText={rgba(91, 175, 211, 255)}
chat_inViews={rgba(153, 153, 153, 255)}
chat_inViewsSelected={rgba(153, 153, 153, 255)}
chat_inVoiceSeekbar={rgba(26, 26, 26, 255)}
chat_inVoiceSeekbarFill={rgba(114, 181, 232, 255)}
chat_inVoiceSeekbarSelected={rgba(191, 223, 246, 255)}
chat_linkSelectBackground={rgba(98, 169, 227, 51)}
chat_lockIcon={white}
chat_mediaBroadcast={white}
chat_mediaInfoText={white}
chat_mediaLoaderPhoto={rgba(0, 0, 0, 102)}
chat_mediaLoaderPhotoIcon={white}
chat_mediaLoaderPhotoIconSelected={rgba(212, 215, 214, 255)}
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
chat_messagePanelVoiceShadow={rgba(0, 0, 0, 0)}
chat_messageTextIn={white}
chat_messageTextOut={white}
chat_muteIcon={rgba(212, 215, 214, 255)}
chat_outAudioCacheSeekbar={rgba(136, 136, 136, 255)}
chat_outAudioDurationSelectedText={rgba(153, 153, 153, 255)}
chat_outAudioDurationText={rgba(153, 153, 153, 255)}
chat_outAudioPerfomerSelectedText={rgba(153, 153, 153, 255)}
chat_outAudioPerfomerText={rgba(153, 153, 153, 255)}
chat_outAudioProgress={rgba(51, 51, 51, 255)}
chat_outAudioSeekbar={rgba(87, 87, 87, 255)}
chat_outAudioSeekbarFill={rgba(136, 136, 136, 255)}
chat_outAudioSeekbarSelected={rgba(136, 136, 136, 255)}
chat_outAudioSelectedProgress={rgba(51, 51, 51, 255)}
chat_outAudioTitleText={rgba(212, 215, 214, 255)}
chat_outBroadcast={rgba(70, 170, 54, 255)}
chat_outBubble={rgba(26, 26, 26, 255)}
chat_outBubbleSelected={rgba(51, 51, 51, 255)}
chat_outBubbleShadow={rgba(0, 0, 0, 0)}
chat_outContactBackground={rgba(212, 215, 214, 255)}
chat_outContactIcon={rgba(51, 51, 51, 255)}
chat_outContactNameText={rgba(81, 154, 186, 255)}
chat_outContactPhoneText={rgba(212, 215, 214, 255)}
chat_outFileBackground={rgba(153, 153, 153, 255)}
chat_outFileBackgroundSelected={rgba(153, 153, 153, 255)}
chat_outFileIcon={rgba(51, 51, 51, 255)}
chat_outFileInfoSelectedText={rgba(153, 153, 153, 255)}
chat_outFileInfoText={rgba(153, 153, 153, 255)}
chat_outFileNameText={rgba(212, 215, 214, 255)}
chat_outFileProgress={rgba(153, 153, 153, 255)}
chat_outFileProgressSelected={rgba(153, 153, 153, 255)}
chat_outFileSelectedIcon={rgba(51, 51, 51, 255)}
chat_outForwardedNameText={rgba(81, 154, 186, 255)}
chat_outInstant={rgba(81, 154, 186, 255)}
chat_outInstantSelected={rgba(81, 154, 186, 255)}
chat_outLoader={rgba(153, 153, 153, 255)}
chat_outLoaderPhoto={rgba(26, 26, 26, 255)}
chat_outLoaderPhotoIcon={rgba(153, 153, 153, 255)}
chat_outLoaderPhotoIconSelected={rgba(212, 215, 214, 255)}
chat_outLoaderPhotoSelected={rgba(51, 51, 51, 255)}
chat_outLoaderSelected={rgba(212, 215, 214, 255)}
chat_outLocationBackground={rgba(212, 215, 214, 255)}
chat_outLocationIcon={rgba(51, 51, 51, 255)}
chat_outMediaIcon={white}
chat_outMediaIconSelected={white}
chat_outMenu={rgba(153, 153, 153, 255)}
chat_outMenuSelected={rgba(153, 153, 153, 255)}
chat_outPreviewInstantSelectedText={rgba(81, 154, 186, 255)}
chat_outPreviewInstantText={rgba(81, 154, 186, 255)}
chat_outPreviewLine={rgba(81, 154, 186, 255)}
chat_outReplyLine={rgba(81, 154, 186, 255)}
chat_outReplyMediaMessageSelectedText={rgba(153, 153, 153, 255)}
chat_outReplyMediaMessageText={rgba(153, 153, 153, 255)}
chat_outReplyMessageText={rgba(153, 153, 153, 255)}
chat_outReplyNameText={rgba(81, 154, 186, 255)}
chat_outSentCheck={white}
chat_outSentCheckRead={white}
chat_outSentCheckSelected={white}
chat_outSentClock={rgba(197, 197, 197, 255)}
chat_outSentClockSelected={rgba(197, 197, 197, 255)}
chat_outSiteNameText={rgba(81, 154, 186, 255)}
chat_outTimeSelectedText={rgba(153, 153, 153, 255)}
chat_outTimeText={rgba(153, 153, 153, 255)}
chat_outVenueInfoSelectedText={rgba(153, 153, 153, 255)}
chat_outVenueInfoText={rgba(153, 153, 153, 255)}
chat_outVenueNameText={rgba(212, 215, 214, 255)}
chat_outViaBotNameText={rgba(58, 140, 207, 255)}
chat_outViews={rgba(153, 153, 153, 255)}
chat_outViewsSelected={rgba(153, 153, 153, 255)}
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
chat_recordVoiceCancel={rgba(153, 153, 153, 255)}
chat_replyPanelClose={rgba(168, 168, 168, 255)}
chat_replyPanelIcons={rgba(77, 166, 234, 255)}
chat_replyPanelLine={rgba(0, 0, 0, 0)}
chat_replyPanelMessage={rgba(212, 215, 214, 255)}
chat_replyPanelName={rgba(58, 140, 207, 255)}
chat_reportSpam={rgba(229, 101, 85, 255)}
chat_searchPanelIcons={rgba(86, 163, 219, 255)}
chat_searchPanelText={rgba(78, 146, 204, 255)}
chat_secretChatStatusText={rgba(99, 99, 99, 255)}
chat_secretTimerBackground={rgba(0, 0, 0, 182)}
chat_secretTimerText={white}
chat_secretTimeText={rgba(212, 215, 214, 255)}
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
chat_topPanelMessage={rgba(212, 215, 214, 255)}
chat_topPanelTitle={rgba(81, 154, 186, 255)}
chat_unreadMessagesStartArrowIcon={rgba(51, 51, 51, 255)}
chat_unreadMessagesStartBackground={rgba(153, 153, 153, 255)}
chat_unreadMessagesStartText={rgba(51, 51, 51, 255)}
chat_wallpaper={black}
chats_actionBackground={rgba(153, 153, 153, 255)}
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
chats_menuCloudBackgroundCats={rgba(153, 153, 153, 255)}
chats_menuItemCheck={rgba(81, 154, 186, 255)}
chats_menuItemIcon={rgba(168, 168, 168, 255)}
chats_menuItemText={rgba(168, 168, 168, 255)}
chats_menuName={white}
chats_menuPhone={rgba(212, 215, 214, 255)}
chats_menuPhoneCats={rgba(212, 215, 214, 255)}
chats_menuTopBackgroundCats={rgba(26, 26, 26, 255)}
chats_menuTopShadow={black}
chats_message={rgba(153, 153, 153, 255)}
chats_muteIcon={rgba(87, 87, 87, 255)}
chats_name={rgba(212, 215, 214, 255)}
chats_nameArchived={rgba(212, 215, 214, 255)}
chats_nameIcon={white}
chats_nameMessage_threeLines={rgba(212, 215, 214, 255)}
chats_nameMessage={rgba(81, 154, 186, 255)}
chats_nameMessageArchived={rgba(153, 153, 153, 255)}
chats_pinnedIcon={rgba(115, 115, 115, 255)}
chats_pinnedOverlay={black}
chats_secretIcon={rgba(113, 215, 86, 255)}
chats_secretName={rgba(113, 215, 86, 255)}
chats_sentCheck={white}
chats_sentClock={rgba(153, 153, 153, 255)}
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
checkboxSquareDisabled={rgba(179, 179, 179, 255)}
checkboxSquareUnchecked={rgba(115, 115, 115, 255)}
contacts_inviteBackground={rgba(85, 190, 97, 255)}
contacts_inviteText={white}
contextProgressInner1={rgba(191, 223, 246, 255)}
contextProgressInner2={rgba(191, 223, 246, 255)}
contextProgressInner3={rgba(179, 179, 179, 255)}
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
dialogCheckboxSquareDisabled={rgba(179, 179, 179, 255)}
dialogCheckboxSquareUnchecked={rgba(115, 115, 115, 255)}
dialogGrayLine={rgba(212, 215, 214, 255)}
dialogIcon={rgba(136, 136, 136, 255)}
dialogInputField={rgba(212, 215, 214, 255)}
dialogInputFieldActivated={rgba(55, 169, 240, 255)}
dialogLineProgress={rgba(82, 125, 163, 255)}
dialogLineProgressBackground={rgba(212, 215, 214, 255)}
dialogLinkSelection={rgba(98, 169, 227, 51)}
dialogProgressCircle={rgba(82, 125, 163, 255)}
dialogRadioBackground={rgba(179, 179, 179, 255)}
dialogRadioBackgroundChecked={rgba(55, 169, 240, 255)}
dialogRoundCheckBox={rgba(62, 193, 249, 255)}
dialogRoundCheckBoxCheck={white}
dialogScrollGlow={rgba(245, 245, 245, 255)}
dialogTextBlack={rgba(245, 245, 245, 255)}
dialogTextBlue={rgba(52, 139, 193, 255)}
dialogTextBlue2={rgba(58, 140, 207, 255)}
dialogTextBlue3={rgba(62, 193, 249, 255)}
dialogTextBlue4={rgba(25, 167, 232, 255)}
dialogTextGray={rgba(52, 139, 193, 255)}
dialogTextGray2={rgba(115, 115, 115, 255)}
dialogTextGray3={rgba(153, 153, 153, 255)}
dialogTextGray4={rgba(179, 179, 179, 255)}
dialogTextHint={rgba(153, 153, 153, 255)}
dialogTextLink={rgba(58, 140, 207, 255)}
dialogTextRed={rgba(205, 90, 90, 255)}
dialogTopBackground={rgba(114, 181, 232, 255)}
divider={rgba(0, 0, 0, 0)}
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
groupcreate_spanText={rgba(245, 245, 245, 255)}
inappPlayerBackground={black}
inappPlayerClose={rgba(87, 87, 87, 255)}
inappPlayerPerformer={rgba(212, 215, 214, 255)}
inappPlayerPlayPause={rgba(98, 176, 235, 255)}
inappPlayerTitle={rgba(212, 215, 214, 255)}
key_chat_messagePanelVoiceLock={rgba(168, 168, 168, 255)}
key_chat_messagePanelVoiceLockBackground={white}
key_chat_messagePanelVoiceLockShadow={black}
key_chats_menuTopShadow={rgba(0, 0, 0, 0)}
key_graySectionText={rgba(212, 215, 214, 255)}
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
picker_disabledButton={rgba(153, 153, 153, 255)}
picker_enabledButton={rgba(25, 167, 232, 255)}
player_actionBar={rgba(26, 26, 26, 255)}
player_actionBarItems={white}
player_actionBarSelector={rgba(26, 26, 26, 255)}
player_actionBarSubtitle={rgba(99, 99, 99, 255)}
player_actionBarTitle={rgba(245, 245, 245, 255)}
player_actionBarTop={rgba(26, 26, 26, 255)}
player_background={black}
player_button={rgba(136, 136, 136, 255)}
player_buttonActive={rgba(41, 182, 247, 255)}
player_placeholder={rgba(51, 51, 51, 255)}
player_placeholderBackground={rgba(245, 245, 245, 255)}
player_progress={rgba(41, 182, 247, 255)}
player_progressBackground={rgba(0, 0, 0, 128)}
player_time={rgba(136, 136, 136, 255)}
profile_actionBackground={rgba(51, 51, 51, 255)}
profile_actionIcon={rgba(212, 215, 214, 255)}
profile_actionPressedBackground={black}
profile_adminIcon={rgba(136, 136, 136, 255)}
profile_creatorIcon={rgba(78, 146, 204, 255)}
profile_status={white}
profile_title={white}
profile_verifiedBackground={rgba(178, 214, 248, 255)}
profile_verifiedCheck={white}
progressCircle={rgba(212, 215, 214, 255)}
radioBackground={rgba(179, 179, 179, 255)}
radioBackgroundChecked={rgba(55, 169, 240, 255)}
returnToCallBackground={rgba(77, 166, 234, 255)}
returnToCallText={white}
sessions_devicesImage={rgba(153, 153, 153, 255)}
sharedMedia_linkPlaceholder={rgba(245, 245, 245, 255)}
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
switchThumbChecked={rgba(245, 245, 245, 255)}
switchTrack={rgba(115, 115, 115, 255)}
switchTrackChecked={rgba(212, 215, 214, 255)}
undo_background={rgba(26, 26, 26, 255)}
windowBackgroundGray={rgba(26, 26, 26, 255)}
windowBackgroundGrayShadow={black}
windowBackgroundWhite={black}
windowBackgroundWhiteBlackText={rgba(212, 215, 214, 255)}
windowBackgroundWhiteBlueHeader={white}
windowBackgroundWhiteBlueText={rgba(81, 154, 186, 255)}
windowBackgroundWhiteBlueText2={rgba(52, 139, 193, 255)}
windowBackgroundWhiteBlueText3={rgba(48, 121, 181, 255)}
windowBackgroundWhiteBlueText4={rgba(78, 146, 204, 255)}
windowBackgroundWhiteBlueText5={rgba(78, 146, 204, 255)}
windowBackgroundWhiteBlueText6={rgba(58, 140, 207, 255)}
windowBackgroundWhiteBlueText7={rgba(48, 121, 181, 255)}
windowBackgroundWhiteGrayIcon={rgba(136, 136, 136, 255)}
windowBackgroundWhiteGrayLine={rgba(212, 215, 214, 255)}
windowBackgroundWhiteGrayText={rgba(99, 99, 99, 255)}
windowBackgroundWhiteGrayText2={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGrayText3={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGrayText4={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGrayText5={rgba(168, 168, 168, 255)}
windowBackgroundWhiteGrayText6={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGrayText7={rgba(197, 197, 197, 255)}
windowBackgroundWhiteGrayText8={rgba(115, 115, 115, 255)}
windowBackgroundWhiteGreenText={rgba(38, 151, 44, 255)}
windowBackgroundWhiteGreenText2={rgba(66, 195, 102, 255)}
windowBackgroundWhiteHintText={rgba(153, 153, 153, 255)}
windowBackgroundWhiteInputField={rgba(212, 215, 214, 255)}
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