<script setup lang="ts">
import { DefaultService, RolesEnum, type UserDocument } from '@/client'
import AuthService from '@/services/AuthService'
import { Notify } from 'quasar'
import { computed, ref } from 'vue'
import UserInfoCard from '@/components/UserInfoCard.vue'
import { useUserStore } from '@/stores/UserStore'

export interface Props {
  user?: UserDocument | null
  editable?: boolean
  isProfile?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isProfile: () => false,
  editable: () => false
})

const currentUser = useUserStore().user

const showEmailDialog = ref(false)
const showPasswordDialog = ref(false)
const showAvatarDialog = ref(false)
const newEmail = ref<string>()
const newPassword = ref<string>('')
const oldPassword = ref<string>('')
const avatarsToChoose = ref<string[]>([])
const newRole = ref<RolesEnum>()

const isAllowedToChangeUserRole = computed(() => {
  return props.user?.role != 'Admin' && currentUser?.role == 'Admin'
})

async function loadAvatarsToChoose() {
  const avatarsResponse = {
    avatars: [
      'https://cdn-icons-png.flaticon.com/512/149/149071.png',
      'https://cdn-icons-png.flaticon.com/512/149/149072.png',
      'https://cdn-icons-png.flaticon.com/512/149/149074.png'
    ]
  }
  avatarsToChoose.value = avatarsResponse.avatars
}

async function handleAvatarUpdate(avatarUrl: string) {
  const updateAvatarResponse = await DefaultService.updateUserUsersUserIdPut(
    props.user._id ?? props.user.id,
    {
      avatar_url: avatarUrl
    }
  )
  Notify.create(
    'Установлен аватар: ' + updateAvatarResponse.user.avatar_url + '. Перезагрузите страницу'
  )
}

async function prepareAvatarDialog() {
  showAvatarDialog.value = true
  await loadAvatarsToChoose()
}

async function handleEmailUpdate() {
  const updateEmailResponse = await DefaultService.updateUserUsersUserIdPut(
    props.user._id ?? props.user.id,
    {
      email: newEmail.value
    }
  )
  Notify.create('Установлен E-mail: ' + updateEmailResponse.user.email + '. Перезагрузите страницу')

  if (props.isProfile) {
    AuthService.update_user_info()
  }
}

async function handlePasswordUpdate() {
  await DefaultService.updateUserPasswordUsersUserIdPasswordPut(props.user._id ?? props.user.id, {
    old_password: oldPassword.value,
    new_password: newPassword.value
  })
  Notify.create('Установлен новый пароль!')
}

async function handleRoleUpdate() {
  await DefaultService.changeUserRoleUsersUserIdRolePut(props.user?._id ?? '', {
    role: newRole.value
  })

  Notify.create('Установлена роль: ' + newRole.value)
}
</script>

<template>
  <q-item v-if="user" class="row justify-start items-start q-pt-lg bg-secondary">
    <UserInfoCard :user="user" class="col" />

    <q-item-section class="col-grow items-start" style="overflow: auto">
      <q-item-label lines="1" class="row text-h5 text-white">
        <div class="q-mr-md">
          {{ user?.email }}
        </div>
        <div v-if="!user?.role" class="text-negative">(Не подтверждена)</div>
      </q-item-label>
      <q-item-label class="text-caption text-white">
        ***Раздел для прочей информации о пользователе***
      </q-item-label>
    </q-item-section>

    <!-- Блок с кнопками для изменения данных -->
    <q-item-actions class="column col-shrink">
      <q-btn
        v-if="editable"
        label="Изменить E-mail"
        @click="showEmailDialog = true"
        class="self-stretch"
        align="left"
        flat
      />
      <q-btn
        v-if="editable"
        label="Изменить пароль"
        @click="showPasswordDialog = true"
        class="self-stretch"
        align="left"
        flat
      />
      <q-btn
        v-if="editable"
        label="Изменить аватар"
        @click="prepareAvatarDialog"
        class="self-stretch"
        align="left"
        flat
      />
      <q-select
        v-if="isAllowedToChangeUserRole"
        v-model="newRole"
        :options="Object.values(RolesEnum)"
        @update:model-value="handleRoleUpdate"
        label="Установить роль"
        class="q-mx-md"
      />
    </q-item-actions>

    <q-dialog v-model="showEmailDialog">
      <q-card class="bg-secondary" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <q-input
            v-model="newEmail"
            label="Новый Email"
            clearable
            :input-style="{ fontSize: '25px' }"
          />
        </q-card-section>

        <q-card-actions align="center" class="bg-secondary text-teal">
          <q-btn label="Изменить" @click="handleEmailUpdate" v-close-popup flat />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showPasswordDialog">
      <q-card class="bg-secondary" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <q-input
            v-model="oldPassword"
            label="Старый пароль"
            v-if="isProfile"
            clearable
            :input-style="{ fontSize: '25px' }"
          />
          <q-input
            v-model="newPassword"
            label="Новый пароль"
            clearable
            :input-style="{ fontSize: '25px' }"
          />
        </q-card-section>

        <q-card-actions align="center" class="bg-secondary text-teal">
          <q-btn label="Изменить" @click="handlePasswordUpdate" v-close-popup flat />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showAvatarDialog">
      <q-card class="bg-secondary" style="width: 100%">
        <q-card-section class="q-pt-lg">
          <!-- Надпись по центру "выберите аватар" -->
          <div class="text-center text-h6 text-white q-mb-md">Выберите аватар</div>
          <q-btn
            v-for="avatarUrl in [...avatarsToChoose, ...avatarsToChoose, ...avatarsToChoose]"
            :key="avatarUrl"
            @click="handleAvatarUpdate(avatarUrl)"
            v-close-popup
            flat
          >
            <img :src="avatarUrl" style="width: 100px" />
          </q-btn>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-item>
</template>
